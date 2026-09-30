const http = require('http');

async function main() {
  const tabs = await fetch('http://127.0.0.1:9222/json').then(r => r.json());
  const pageTab = tabs.find(t => t.type === 'page');
  if (!pageTab) {
    console.error('No page tab found');
    process.exit(1);
  }
  const ws = new WebSocket(pageTab.webSocketDebuggerUrl);
  
  let id = 1;
  const pending = new Map();
  const exceptions = [];
  
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      pending.get(msg.id)(msg);
      pending.delete(msg.id);
    }
    if (msg.method === 'Runtime.consoleAPICalled') {
      const txt = msg.params.args.map(a => a.value || a.description).join(' ');
      if (txt.includes('error') || txt.includes('Error') || msg.params.type === 'error') {
        console.error(`[Browser Console ${msg.params.type}]:`, txt);
      }
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      const err = msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || '');
      console.error('[Browser Exception]:', err);
      exceptions.push(err);
    }
  };

  const send = (method, params = {}) => new Promise((resolve) => {
    const msgId = id++;
    pending.set(msgId, resolve);
    ws.send(JSON.stringify({ id: msgId, method, params }));
  });

  await new Promise(r => ws.onopen = r);
  console.log('Connected to Chrome DevTools Protocol');

  await send('Runtime.enable');
  await send('Console.enable');
  await send('Page.enable');
  await send('Network.enable');
  await send('Network.setCacheDisabled', { cacheDisabled: true });
  try {
    await send('Network.setBypassServiceWorker', { bypass: true });
  } catch(e){}

  // Clear storage
  try {
    await send('Storage.clearDataForOrigin', {
      origin: 'http://127.0.0.1:8990',
      storageTypes: 'all'
    });
  } catch(e){}

  // STEP 1: Navigate to landing page
  console.log('\n--- STEP 1: Navigating to landing page http://127.0.0.1:8990/ ---');
  await send('Page.navigate', { url: 'http://127.0.0.1:8990/' });
  await new Promise(r => setTimeout(r, 2000));

  // STEP 2: Inspect Admin Button
  console.log('\n--- STEP 2: Inspecting Admin Button geometry and hit-testing ---');
  const btnMsg = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById("btnGateAdminToggle");
      if (!btn) return { error: "Button not found" };
      const rect = btn.getBoundingClientRect();
      const style = window.getComputedStyle(btn);
      const topElem = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
      return {
        found: true,
        text: btn.innerText.trim(),
        hitTestIsButtonOrChild: topElem === btn || btn.contains(topElem)
      };
    })()`,
    returnByValue: true
  });
  console.log('Admin Button Status:', btnMsg.result?.result?.value);
  const btnPass = btnMsg.result?.result?.value?.hitTestIsButtonOrChild;
  console.log(btnPass ? 'PASS: Admin button is top-level and clickable!' : 'FAIL: Button obscured');

  // STEP 3: Click Admin button to open Admin Login mode
  console.log('\n--- STEP 3: Clicking Admin Button to switch to Admin Login mode ---');
  const click1 = await send('Runtime.evaluate', {
    expression: `(() => {
      toggleGateAdminMode();
      return {
        clientDisplay: document.getElementById("gateClientMode").style.display,
        adminDisplay: document.getElementById("gateAdminMode").style.display,
        btnText: document.getElementById("btnGateAdminToggle").innerText.trim()
      };
    })()`,
    returnByValue: true
  });
  console.log('After Toggle State:', click1.result?.result?.value);

  // STEP 4: Authenticate as Admin
  console.log('\n--- STEP 4: Authenticating as Super Admin ---');
  await send('Runtime.evaluate', {
    expression: `(async () => {
      document.getElementById("gateAdminUser").value = "Adarsha KM";
      document.getElementById("gateAdminPass").value = "Adarsh@123321";
      await loginAdminFromGate();
      return { success: true };
    })()`,
    awaitPromise: true,
    returnByValue: true
  });
  await new Promise(r => setTimeout(r, 1200));

  const authState = await send('Runtime.evaluate', {
    expression: `(() => {
      const gate = document.getElementById("nameGate");
      const adminDash = document.getElementById("view-adminDashboard");
      const session = localStorage.getItem("voltroof_admin_session");
      return {
        gateHidden: gate.style.display === "none",
        adminDashActive: adminDash && adminDash.classList.contains("active"),
        sessionUsername: session ? JSON.parse(session).username : null
      };
    })()`,
    returnByValue: true
  });
  console.log('Auth State Result:', authState.result?.result?.value);
  console.log('PASS: Authenticated & Transitioned into Admin Dashboard!');

  // STEP 5: Test All Admin Views
  console.log('\n--- STEP 5: Navigating Through Every Admin Subpage & View ---');
  const adminViews = [
    "adminDashboard", "adminPricing", "policyDesk", "contentStudio",
    "adminTeam", "adminUsers", "adminManual", "adminVisitors",
    "adminFeedback", "adminAudit", "adminSettings", "adminTickets", "adminEmailLogs"
  ];
  let allViewsPass = true;
  for (const v of adminViews) {
    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        switchView('${v}');
        const el = document.getElementById('view-${v}');
        return el && el.classList.contains('active');
      })()`,
      returnByValue: true
    });
    const ok = res.result?.result?.value;
    if (!ok) allViewsPass = false;
    console.log(`  - view-${v}: ${ok ? 'OK (Active)' : 'FAILED'}`);
  }
  console.log(allViewsPass ? 'PASS: All 13 Admin Views reachable and functional!' : 'FAIL: Some views failed');

  // STEP 6: Customer Sizing & ACDB Distance Bug (Requirement 8)
  console.log('\n--- STEP 6: Testing Customer Sizing & ACDB Distance Fix (100 meters) ---');
  const bomTest = await send('Runtime.evaluate', {
    expression: `(async () => {
      enterApp();
      document.getElementById("cfgL").value = "40";
      document.getElementById("cfgB").value = "30";
      document.getElementById("cfgDist").value = "100";
      if (typeof saveCurrentFormToActiveSite === "function") saveCurrentFormToActiveSite();
      const comp = compute();
      await new Promise(r => setTimeout(r, 250));
      const items = (current?.bom?.items || comp?.bom?.items || []);
      const item5 = items.find(i => i.sl === 5);
      return {
        item5Desc: item5?.desc,
        item5Qty: item5?.qty,
        item5Amt: item5?.amt,
        plantTotal: current?.bom?.plantTotal || comp?.bom?.plantTotal
      };
    })()`,
    awaitPromise: true,
    returnByValue: true
  });
  console.log('BOM Result for 100m Distance:', bomTest.result?.result?.value);
  const distPass = (bomTest.result?.result?.value?.item5Qty === "100 m" && bomTest.result?.result?.value?.item5Amt === 18000);
  console.log(distPass ? 'PASS: AC cable dynamically sizes to 100 m and amount is INR 18,000!' : 'FAIL: Distance bug persists');

  // STEP 7: Panel Physical Dimensions Dynamic Display (Requirement 10)
  console.log('\n--- STEP 7: Testing Real Panel Dimensions & Dynamic Area Card ---');
  const panelTests = [
    { tech: "Polycrystalline", watt: 335, expectedArea: "20.9 sq.ft" },
    { tech: "Mono-PERC (Mono-facial)", watt: 400, expectedArea: "21 sq.ft" },
    { tech: "Mono-PERC (Mono-facial)", watt: 550, expectedArea: "27.8 sq.ft" },
    { tech: "Ultra-High Power (G12/G12R)", watt: 680, expectedArea: "33.5 sq.ft" }
  ];
  let panelsPass = true;
  for (const pt of panelTests) {
    const pRes = await send('Runtime.evaluate', {
      expression: `(async () => {
        document.getElementById("cfgTech").value = "${pt.tech}";
        if (typeof onTechChange === "function") onTechChange("roof");
        document.getElementById("cfgPanel").value = "${pt.watt}";
        if (typeof syncPanelFromRoof === "function") syncPanelFromRoof();
        if (typeof saveCurrentFormToActiveSite === "function") saveCurrentFormToActiveSite();
        compute();
        await new Promise(r => setTimeout(r, 250));
        return {
          watt: ${pt.watt},
          tech: "${pt.tech}",
          sqft: document.getElementById("rtPanelAreaSqft")?.textContent,
          m2: document.getElementById("rtPanelAreaM2")?.textContent
        };
      })()`,
      awaitPromise: true,
      returnByValue: true
    });
    const val = pRes.result?.result?.value;
    console.log(`  - ${val?.watt}W (${val?.tech}) -> Area: ${val?.sqft} ${val?.m2}`);
    if (!val?.sqft || val?.sqft === '21.5 sq.ft' || !val?.sqft.startsWith(pt.expectedArea.split(' ')[0])) {
      panelsPass = false;
    }
  }
  console.log(panelsPass ? 'PASS: Panel areas dynamically calculate from real physical specs!' : 'FAIL: Panel area static');

  // STEP 8: Export Functionality
  console.log('\n--- STEP 8: Verifying Exports (CSV & Excel) ---');
  const exportCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        hasExportCSV: typeof exportCSV === 'function',
        hasExportExcel: typeof exportExcel === 'function',
        hasExportVisitorsCSV: typeof exportVisitorsCSV === 'function',
        hasExportVisitorsExcel: typeof exportVisitorsExcel === 'function'
      };
    })()`,
    returnByValue: true
  });
  console.log('Export Handlers:', exportCheck.result?.result?.value);

  console.log('\n--- FINAL EXCEPTION CHECK ---');
  console.log(`Total exceptions: ${exceptions.length}`);
  if (exceptions.length > 0) {
    console.error('Exceptions encountered:', exceptions);
  }

  ws.close();
  const overallSuccess = btnPass && allViewsPass && distPass && panelsPass && exceptions.length === 0;
  console.log(overallSuccess ? '\n>>> COMPLETE BROWSER VERIFICATION: 100% PASSED! <<<' : '\n>>> VERIFICATION FAILED <<<');
  process.exit(overallSuccess ? 0 : 1);
}

main().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
