let teacherToDelete = null;

function openModal(id) {
  document.getElementById(id).style.display = "flex";
}

function closeModal(id) {
  document.getElementById(id).style.display = "none";
}

function openUpdateModal(id, name) {
  document.getElementById("update_teacher_id").value = id;
  document.getElementById("update_name").value = name;
  openModal("updateModal");
}

function openDeleteModal(id, name) {
  teacherToDelete = id;
  document.getElementById("deleteTeacherName").textContent = `Are you sure you want to delete "${name}"?`;
  openModal("deleteModal");
}

document.addEventListener("DOMContentLoaded", () => {
  // Attach delete buttons
  document.querySelectorAll("a.delete").forEach(btn => {
    btn.addEventListener("click", () => {
      openDeleteModal(btn.dataset.id, btn.dataset.name);
    });
  });

  // Confirm delete
  document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
    if (!teacherToDelete) return;
    const response = await fetch(`/admin/delete-teacher/${teacherToDelete}`, { method: "DELETE" });
    closeModal("deleteModal");
    teacherToDelete = null;
    if (response.ok) location.reload();
    else alert("Failed to delete teacher.");
  });

  // Add teacher
  document.getElementById("addForm").onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch("/admin/add-teacher", { method: "POST", body: formData });
    if (response.ok) location.reload();
    else alert("Failed to add teacher.");
  };

  // Update teacher
  document.getElementById("updateForm").onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch("/admin/update-teacher", { method: "POST", body: formData });
    if (response.ok) location.reload();
    else alert("Failed to update teacher.");
  };
});
