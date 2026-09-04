from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''  var RETURN_COUNT_KEY = "pdh_return_count_v3";\n\n  function getReturnCount(){\n    try { return Math.max(0, Number(localStorage.getItem(RETURN_COUNT_KEY) || 0)); }\n    catch(e){ return 0; }\n  }\n\n  function setReturnCount(n){\n    try { localStorage.setItem(RETURN_COUNT_KEY, String(n)); } catch(e){}\n  }\n\n  function incrementReturnCount(){\n    var n = getReturnCount() + 1;\n    setReturnCount(n);\n    return n;\n  }\n'''
new='''  var returnCount = 0;\n\n  function getReturnCount(){\n    return returnCount;\n  }\n\n  function incrementReturnCount(){\n    returnCount += 1;\n    return returnCount;\n  }\n'''
if old not in s:
    raise SystemExit('bloco de contagem nao encontrado')
s=s.replace(old,new,1)
s=s.replace('fifthTryMode = getReturnCount() === 5;','fifthTryMode = getReturnCount() === 5;',1)
p.write_text(s,encoding='utf-8')
print('ok')
