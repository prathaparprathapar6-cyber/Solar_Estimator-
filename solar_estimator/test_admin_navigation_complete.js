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

  // Clear all storage for origin
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

  // STEP 2: Check Admin button inspection
  console.log('\n--- STEP 2: Inspecting Admin Button geometry and click hit-testing ---');
  const btnMsg = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById("btnGateAdminToggle");
      if (!btn) return { error: "Button not found" };
      const rect = btn.getBoundingClientRect();
      const style = window.getComputedStyle(btn);
      const centerX = rect.x + rect.width / 2;
      const centerY = rect.y + rect.height / 2;
      const topElem = document.elementFromPoint(centerX, centerY);
      return {
        found: true,
        text: btn.innerText.trim(),
        rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
        display: style.display,
        visibility: style.visibility,
        pointerEvents: style.pointerEvents,
        zIndex: style.zIndex,
        hitTestTag: topElem ? topElem.tagName : null,
        hitTestId: topElem ? topElem.id : null,
        hitTestIsButtonOrChild: topElem === btn || btn.contains(topElem)
      };
    })()`,
    returnByValue: true
  });
  console.log('Admin Button Status:', btnMsg.result?.result?.value);
  if (!btnMsg.result?.result?.value?.hitTestIsButtonOrChild) {
    console.error('FAIL: Admin button is obscured by another element!');
  } else {
    console.log('PASS: Admin button is top-level and directly clickable!');
  }

  // STEP 3: Click Admin button to open Admin Login mode
  console.log('\n--- STEP 3: Clicking Admin Button to switch to Admin Login mode ---');
  const click1 = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById("btnGateAdminToggle");
      btn.click();
      return {
        clientModeDisplay: document.getElementById("gateClientMode").style.display,
        adminModeDisplay: document.getElementById("gateAdminMode").style.display,
        adminLoginFormDisplay: document.getElementById("gateAdminLoginForm").style.display,
        btnText: btn.innerText.trim(),
        activeElementId: document.activeElement ? document.activeElement.id : null
      };
    })()`,
    returnByValue: true
  });
  console.log('After Click 1 State:', click1.result?.result?.value);
  const state1 = click1.result?.result?.value;
  if (state1.clientModeDisplay === 'none' && state1.adminModeDisplay === 'block' && state1.adminLoginFormDisplay === 'block') {
    console.log('PASS: Admin Sign In form opened successfully!');
  } else {
    console.error('FAIL: Admin form did not open properly!');
  }

  // Wait for debounce window (250ms)
  await new Promise(r => setTimeout(r, 250));

  // STEP 4: Click button again to test toggle back to User mode
  console.log('\n--- STEP 4: Clicking button again to switch back to User Mode ---');
  const click2 = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById("btnGateAdminToggle");
      btn.click();
      return {
        clientModeDisplay: document.getElementById("gateClientMode").style.display,
        adminModeDisplay: document.getElementById("gateAdminMode").style.display,
        btnText: btn.innerText.trim()
      };
    })()`,
    returnByValue: true
  });
  console.log('After Click 2 State:', click2.result?.result?.value);
  const state2 = click2.result?.result?.value;
  if (state2.clientModeDisplay === 'block' && state2.adminModeDisplay === 'none') {
    console.log('PASS: Successfully toggled back to User Mode!');
  } else {
    console.error('FAIL: Could not toggle back to User Mode!');
  }

  // Wait for debounce window (250ms)
  await new Promise(r => setTimeout(r, 250));

  // STEP 5: Re-open Admin Login mode and test Authentication
  console.log('\n--- STEP 5: Switching to Admin Mode & Performing Authentication ---');
  await send('Runtime.evaluate', {
    expression: `document.getElementById("btnGateAdminToggle").click();`
  });
  await new Promise(r => setTimeout(r, 200));

  // Fill in credentials and authenticate
  const authRes = await send('Runtime.evaluate', {
    expression: `(async () => {
      document.getElementById("gateAdminUser").value = "Adarsha KM";
      document.getElementById("gateAdminPass").value = "Adarsh@123321";
      await loginAdminFromGate();
      return { success: true };
    })()`,
    awaitPromise: true,
    returnByValue: true
  });
  console.log('Authentication triggered:', authRes.result?.result?.value);

  // Wait 1.5 seconds for entrance transition
  console.log('Waiting for gate transition to Admin Dashboard...');
  await new Promise(r => setTimeout(r, 1500));

  const postAuth = await send('Runtime.evaluate', {
    expression: `(() => {
      const gate = document.getElementById("nameGate");
      const adminDash = document.getElementById("view-adminDashboard");
      const session = localStorage.getItem("voltroof_admin_session");
      const hasAdminModeClass = document.body.classList.contains("admin-mode");
      return {
        gateHidden: gate.style.display === "none" || gate.classList.contains("hidden"),
        hasAdminModeClass: hasAdminModeClass,
        adminDashDisplay: adminDash ? window.getComputedStyle(adminDash).display : null,
        sessionStored: !!session,
        sessionUsername: session ? JSON.parse(session).username : null
      };
    })()`,
    returnByValue: true
  });
  console.log('Post-Authentication State:', postAuth.result?.result?.value);
  const authState = postAuth.result?.result?.value;
  if (authState.gateHidden && authState.hasAdminModeClass && authState.adminDashDisplay !== 'none' && authState.sessionStored) {
    console.log('PASS: Complete Authentication Flow Successful! Admin Dashboard Opened!');
  } else {
    console.error('FAIL: Admin Dashboard was not properly opened post-auth!');
  }

  // STEP 6: Test direct navigation to /admin route
  console.log('\n--- STEP 6: Testing direct URL navigation to /admin ---');
  await send('Page.navigate', { url: 'http://127.0.0.1:8990/admin' });
  await new Promise(r => setTimeout(r, 2000));

  const adminRouteCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const gate = document.getElementById("nameGate");
      const adminMode = document.getElementById("gateAdminMode");
      const clientMode = document.getElementById("gateClientMode");
      return {
        url: window.location.href,
        gateExists: !!gate,
        adminModeVisible: adminMode && adminMode.style.display !== "none"
      };
    })()`,
    returnByValue: true
  });
  console.log('Direct /admin Route Check:', adminRouteCheck.result?.result?.value);
  if (adminRouteCheck.result?.result?.value?.adminModeVisible) {
    console.log('PASS: Direct /admin route correctly opens Admin Login Mode!');
  }

  console.log('\n--- FINAL EXCEPTION CHECK ---');
  if (exceptions.length === 0) {
    console.log('PASS: Zero exceptions thrown during entire navigation and login cycle!');
  } else {
    console.error(`FAIL: ${exceptions.length} exceptions were encountered:`, exceptions);
  }

  ws.close();
  const allPassed = (
    btnMsg.result?.result?.value?.hitTestIsButtonOrChild &&
    state1.clientModeDisplay === 'none' && state1.adminModeDisplay === 'block' && state1.adminLoginFormDisplay === 'block' &&
    state2.clientModeDisplay === 'block' && state2.adminModeDisplay === 'none' &&
    authState.gateHidden && authState.hasAdminModeClass && authState.adminDashDisplay !== 'none' && authState.sessionStored &&
    adminRouteCheck.result?.result?.value?.adminModeVisible &&
    exceptions.length === 0
  );
  process.exit(allPassed ? 0 : 1);
}

main().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
