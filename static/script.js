function updateHeader(counts) {
  document.getElementById("pending-count").innerText = counts.pending;
  document.getElementById("progress-count").innerText = counts.progress;
  document.getElementById("completed-count").innerText = counts.completed;
  document.getElementById("total-count").innerText = counts.total;
}

function allowDrop(e) { e.preventDefault(); }

function drag(e) { e.dataTransfer.setData("task-id", e.target.dataset.taskId); }

function handleDrop(e) {
  e.preventDefault();
  const taskId = e.dataTransfer.getData("task-id");
  const newStatus = e.currentTarget.getAttribute("data-status");
  const taskCard = document.querySelector(`[data-task-id="${taskId}"]`);
  e.currentTarget.appendChild(taskCard);

  fetch(`/update_status/${taskId}`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `status=${newStatus}`
  })
  .then(res => res.json())
  .then(data => { if (data.success) updateHeader(data.counts); });
}

function deleteTask(taskId) {
  if (!confirm("⚠️ Are you sure you want to delete this task?")) return;
  fetch(`/delete/${taskId}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.querySelector(`[data-task-id="${taskId}"]`).remove();
        updateHeader(data.counts);
      }
    });
}
