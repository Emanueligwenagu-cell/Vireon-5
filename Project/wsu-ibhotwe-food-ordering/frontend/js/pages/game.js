const WIN_COMBOS=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];

function checkWinner(board){
  for(const combo of WIN_COMBOS){
    const [a,b,c]=combo;
    if(board[a]&&board[a]===board[b]&&board[a]===board[c]) return{winner:board[a],combo};
  }
  return{winner:null,combo:null};
}

function minimax(board,isMax,depth,alpha,beta){
  const {winner}=checkWinner(board);
  if(winner==='O') return 10-depth;
  if(winner==='X') return depth-10;
  if(board.every(c=>c!==null)) return 0;
  if(isMax){
    let best=-Infinity;
    for(let i=0;i<9;i++){if(!board[i]){board[i]='O';best=Math.max(best,minimax(board,false,depth+1,alpha,beta));board[i]=null;alpha=Math.max(alpha,best);if(beta<=alpha) break;}}
    return best;
  } else {
    let best=Infinity;
    for(let i=0;i<9;i++){if(!board[i]){board[i]='X';best=Math.min(best,minimax(board,true,depth+1,alpha,beta));board[i]=null;beta=Math.min(beta,best);if(beta<=alpha) break;}}
    return best;
  }
}

function getAIMove(board,diff){
  const empty=board.map((v,i)=>v===null?i:-1).filter(i=>i!==-1);
  if(diff==='easy'&&Math.random()<0.7) return empty[Math.floor(Math.random()*empty.length)];
  if(diff==='medium'&&Math.random()<0.3) return empty[Math.floor(Math.random()*empty.length)];
  let bestScore=-Infinity,bestMove=empty[0];
  const bc=[...board];
  for(const i of empty){bc[i]='O';const s=minimax(bc,false,0,-Infinity,Infinity);bc[i]=null;if(s>bestScore){bestScore=s;bestMove=i;}}
  return bestMove;
}

function renderGame(){
  const g=state.game;
  const {winner,combo}=checkWinner(g.board);
  const isDraw=!winner&&g.board.every(c=>c!==null);
  const gameOver=!!winner||isDraw;
  const modeLabel=(p)=>g.mode==='pvc'?(p==='X'?'You':'AI'):('Player '+p);
  return `
  <div class="game-outer">
    <div class="game-header">
      <div class="game-waiting-badge">🎮 Play While You Wait!</div>
      <h1>Tic-Tac-Toe</h1>
      <p>Challenge a friend or face the AI</p>
    </div>
    <!-- Settings -->
    <div class="game-settings">
      <div class="game-settings-grid">
        <div>
          <div class="game-setting-label">Game Mode</div>
          <div class="toggle-group">
            <button class="toggle-opt${g.mode==='pvp'?' active':''}" onclick="setGameMode('pvp')">👥 2 Players</button>
            <button class="toggle-opt${g.mode==='pvc'?' active':''}" onclick="setGameMode('pvc')">🤖 vs AI</button>
          </div>
        </div>
        ${g.mode==='pvc'?`
        <div>
          <div class="game-setting-label">AI Difficulty</div>
          <div class="toggle-group">
            <button class="toggle-opt easy${g.difficulty==='easy'?' active':''}" onclick="setGameDiff('easy')">Easy</button>
            <button class="toggle-opt medium${g.difficulty==='medium'?' active':''}" onclick="setGameDiff('medium')">Medium</button>
            <button class="toggle-opt hard${g.difficulty==='hard'?' active':''}" onclick="setGameDiff('hard')">Hard</button>
          </div>
        </div>`:''}
      </div>
    </div>
    <!-- Scoreboard -->
    <div class="scoreboard">
      <div class="score-card${!gameOver&&g.current==='X'?' turn':''}">
        <div class="score-emoji">❌</div>
        <div class="score-val x">${g.scores.X}</div>
        <div class="score-name">${escHtml(modeLabel('X'))}</div>
      </div>
      <div class="score-card">
        <div class="score-emoji">🤝</div>
        <div class="score-val d">${g.scores.draw}</div>
        <div class="score-name">Draw</div>
      </div>
      <div class="score-card${!gameOver&&g.current==='O'?' turn':''}">
        <div class="score-emoji">⭕</div>
        <div class="score-val o">${g.scores.O}</div>
        <div class="score-name">${escHtml(modeLabel('O'))}</div>
      </div>
    </div>
    <!-- Status -->
    <div class="game-status">
      ${gameOver
        ? (winner
          ? `<span>🏆</span><span style="color:${winner==='X'?'var(--orange)':'var(--purple)'};font-weight:900;font-size:18px">${escHtml(modeLabel(winner))} wins! 🎉</span>`
          : `<span style="font-weight:900;font-size:18px;color:var(--gray-500)">It's a draw! 🤝</span>`)
        : (g.thinking
          ? `<div class="thinking"><div class="spinner"></div>AI is thinking...</div>`
          : `<span class="${g.current==='X'?'player-x':'player-o'}">${g.current==='X'?'❌':'⭕'} ${escHtml(modeLabel(g.current))}'s turn</span>`)}
    </div>
    <!-- Board -->
    <div class="board-wrap">
      <div class="board">
        ${g.board.map((cell,i)=>{
          const isWin=combo&&combo.includes(i);
          const cls=['cell'];
          if(cell) cls.push('filled');
          if(cell==='X') cls.push('x-cell');
          if(cell==='O') cls.push('o-cell');
          if(isWin&&winner==='X') cls.push('win-x');
          if(isWin&&winner==='O') cls.push('win-o');
          if(gameOver) cls.push('game-over');
          return `<div class="${cls.join(' ')}" id="cell-${i}" onclick="cellClick(${i})">
            ${cell?`<span style="display:inline-block;animation:popIn .15s ease-out;color:${cell==='X'?'var(--orange)':'var(--purple)'}">${cell==='X'?'✕':'○'}</span>`:''}
          </div>`;
        }).join('')}
      </div>
    </div>
    <!-- Actions -->
    <div class="game-actions">
      <button class="btn btn-outline btn-full" onclick="resetGame()">↺ New Game</button>
      <button class="btn btn-primary btn-full" onclick="resetAllScores()">🏆 Reset Scores</button>
    </div>
    <!-- Links -->
    <div class="game-links">
      <button class="btn btn-outline btn-full" onclick="navigate('home')">🏠 Back Home</button>
      <button class="btn btn-dark btn-full" onclick="navigate('orders')">📦 Check My Order</button>
    </div>
    <div class="game-how">
      <p>How to Play</p>
      <p>Get 3 in a row — horizontally, vertically, or diagonally — to win!${g.mode==='pvc'?' You are ❌, the AI is ⭕.':''}</p>
    </div>
  </div>`;
}

function bindGame(){
  // Board cells already have onclick via HTML
}

function cellClick(idx){
  const g=state.game;
  if(g.board[idx]||g.gameOver||g.thinking) return;
  if(g.mode==='pvc'&&g.current==='O') return;
  g.board[idx]=g.current;
  const {winner,combo}=checkWinner(g.board);
  if(winner){
    g.winner=winner;g.winCombo=combo;g.gameOver=true;g.scores[winner]++;
    refreshGame();return;
  }
  if(g.board.every(c=>c!==null)){
    g.gameOver=true;g.scores.draw++;refreshGame();return;
  }
  const next=g.current==='X'?'O':'X';
  g.current=next;
  if(g.mode==='pvc'&&next==='O'){
    g.thinking=true;refreshGame();
    setTimeout(()=>{
      const mv=getAIMove([...g.board],g.difficulty);
      g.board[mv]='O';
      const res=checkWinner(g.board);
      if(res.winner){g.winner=res.winner;g.winCombo=res.combo;g.gameOver=true;g.scores['O']++;}
      else if(g.board.every(c=>c!==null)){g.gameOver=true;g.scores.draw++;}
      else{g.current='X';}
      g.thinking=false;refreshGame();
    },400);
  } else {
    refreshGame();
  }
}

function resetGame(){
  const g=state.game;
  g.board=Array(9).fill(null);g.current='X';g.gameOver=false;
  g.winner=null;g.winCombo=null;g.thinking=false;
  refreshGame();
}
function resetAllScores(){
  resetGame();state.game.scores={X:0,O:0,draw:0};refreshGame();
}
function setGameMode(m){state.game.mode=m;resetGame();}
function setGameDiff(d){state.game.difficulty=d;resetGame();}
function refreshGame(){
  const el=document.getElementById('game-page');
  el.innerHTML=renderGame();bindGame();
}

