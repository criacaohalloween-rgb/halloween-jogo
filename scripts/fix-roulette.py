from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
start_marker = '  /* ================= GAME 3: ROLETA ================= */'
end_marker = '  /* ================= EVENTOS GERAIS ================= */'
start = text.find(start_marker)
end = text.find(end_marker, start + len(start_marker))
if start < 0 or end < 0:
    raise SystemExit('Bloco da roleta não encontrado')

block = '''  /* ================= GAME 3: ROLETA ================= */
  var NORMAL_WHEEL_LABELS = ["TICKET","VOLTE\\nAO INÍCIO","TENTE\\nDE NOVO","TICKET","VOLTE\\nAO INÍCIO","TENTE\\nDE NOVO"];
  var WHEEL_LABELS = NORMAL_WHEEL_LABELS.slice();
  var fifthTryMode = false;
  var g3 = { spinning:false, totalRotation:0 };
  var RETURN_COUNT_KEY = "pdh_return_count_v3";

  function getReturnCount(){
    try { return Math.max(0, Number(localStorage.getItem(RETURN_COUNT_KEY) || 0)); }
    catch(e){ return 0; }
  }

  function setReturnCount(n){
    try { localStorage.setItem(RETURN_COUNT_KEY, String(n)); } catch(e){}
  }

  function incrementReturnCount(){
    var n = getReturnCount() + 1;
    setReturnCount(n);
    return n;
  }

  function initGame3(){
    g3.spinning = false;
    fifthTryMode = getReturnCount() === 5;
    WHEEL_LABELS = fifthTryMode ? ["TICKET","TICKET","TICKET","TICKET","TICKET","TICKET"] : NORMAL_WHEEL_LABELS.slice();
    document.getElementById("wheelResult").textContent = "";
    var btn = document.getElementById("spinBtn");
    btn.disabled = false;
    btn.textContent = "GIRAR";
    rebuildWheelLabels();
    if(fifthTryMode){
      setTimeout(function(){
        sayLine("JÁ TEM 5 VEZES QUE VOCÊ TENTA, VOU FACILITAR PRA VOCÊ.", 3000);
      }, 650);
    }
  }

  function rebuildWheelLabels(){
    var wheel = document.getElementById("wheel");
    wheel.querySelectorAll(".slice-label").forEach(function(el){ el.remove(); });
    WHEEL_LABELS.forEach(function(label, i){
      var mid = i*60 + 30;
      var span = document.createElement("div");
      span.className = "slice-label";
      span.style.transform = "rotate(" + mid + "deg) translateY(-92px)";
      span.innerHTML = label.replace("\\n", "<br>");
      wheel.appendChild(span);
    });
  }

  function chooseWheelOutcome(){
    if(fifthTryMode) return "TICKET";
    var roll = Math.random();
    if(roll < 0.50) return "VOLTE";
    if(roll < 0.80) return "TENTE";
    return "TICKET";
  }

  function chooseWheelIndex(outcome){
    var pool = outcome === "TICKET" ? [0,3] : outcome === "VOLTE" ? [1,4] : [2,5];
    return pool[Math.floor(Math.random()*pool.length)];
  }

  function spinWheel(){
    if(g3.spinning) return;
    g3.spinning = true;
    document.getElementById("spinBtn").disabled = true;
    var outcome = chooseWheelOutcome();
    var idx = chooseWheelIndex(outcome);
    var mid = idx*60 + 30;
    var prev = g3.totalRotation;
    var base = prev - (prev % 360);
    var newTotal = base + 360*5 + (360 - mid);
    g3.totalRotation = newTotal;
    document.getElementById("wheel").style.transform = "rotate(" + newTotal + "deg)";
    setTimeout(function(){ evaluateWheel(idx); }, 4300);
  }

  function evaluateWheel(idx){
    g3.spinning = false;
    var label = WHEEL_LABELS[idx];
    var resultEl = document.getElementById("wheelResult");
    if(label === "TICKET"){
      resultEl.textContent = "🎟️ Ticket conquistado!";
      if(fifthTryMode){
        playSfx("sfxWin");
        sayLine("AGORA NÃO TEM COMO VOCÊ ERRAS.", 2600);
        setTimeout(function(){ goTo("final"); showFinalResult(); }, 1500);
      }else{
        winGame("game3");
      }
    }
    else if(label.indexOf("TENTE") === 0){
      resultEl.textContent = "Tente novamente!";
      playSfx("sfxLaugh");
      sayLine(randomTaunt());
      document.getElementById("spinBtn").disabled = false;
    }
    else{
      var count = incrementReturnCount();
      resultEl.textContent = "De volta ao início...";
      playSfx("sfxLaugh");
      if(count === 3){
        sayLine("AH, VOCÊ JÁ PASSOU AQUI 3 VEZES...", 2600);
      }else{
        sayLine(randomTaunt(), 2600);
      }
      setTimeout(function(){ goTo("game1"); }, 1800);
    }
  }

'''
new_text = text[:start] + block + text[end:]
path.write_text(new_text, encoding='utf-8')
print('Roleta corrigida.')
