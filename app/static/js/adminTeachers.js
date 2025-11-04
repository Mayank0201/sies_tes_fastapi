async function deleteTeacher(id) {
  const response = await fetch(`/admin/delete-teacher/${id}`, { method: "DELETE" });
  if (response.ok) location.reload();
  else alert("Failed to delete teacher.");
}

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

document.getElementById("addForm").onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch("/admin/add-teacher", { method: "POST", body: formData });
  if (response.ok) location.reload();
  else alert("Failed to add teacher.");
};

document.getElementById("updateForm").onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch("/admin/update-teacher", { method: "POST", body: formData });
  if (response.ok) location.reload();
  else alert("Failed to update teacher.");
};
