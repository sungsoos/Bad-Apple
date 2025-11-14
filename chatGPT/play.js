// === CONFIG ===
const FPS = 12;

try {
  FRAMES;
}
catch (error) {
  if (ReferenceError) {
    FRAMES = [`You should run badapple_frames.js first!`]
  } else {
    FRAMES = [error]
  }
}
  

// === GET LAST ASSISTANT MESSAGE ===
function getLatestAssistantMessage() {
  const nodes = document.querySelectorAll("*[data-message-author-role='assistant']");
  return nodes[nodes.length - 1];
}

let target = getLatestAssistantMessage();

if (!target) {
  console.error("could not find latest message.");
} else {
  target.style.whiteSpace = "pre";
  target.style.fontFamily = "monospace";
  target.style.fontSize = "10px";
}

// === PLAYER ===
let index = 0;
function playFrame() {
  const latest = getLatestAssistantMessage();
  if (latest && latest !== target) {
    target = latest;
    target.style.whiteSpace = "pre";
    target.style.fontFamily = "monospace";
    target.style.fontSize = "12px";
  }

  if (target) {
    target.textContent = FRAMES[index];
    index = (index + 1) % FRAMES.length;
  }
}

console.log("Started.");
setInterval(playFrame, 1000 / FPS);