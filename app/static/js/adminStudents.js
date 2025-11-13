function openModal(id) {
  document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}

function openUpdateModal(id, name, roll, classId, year, courseId, eligible) {
  document.getElementById('update_student_id').value = id;
  document.getElementById('update_name').value = name;
  document.getElementById('update_roll_no').value = roll;
  document.getElementById('update_class_id').value = classId;
  document.getElementById('update_admission_year').value = year;
  document.getElementById('update_course_id').value = courseId;
  document.getElementById('update_is_eligible').value = eligible;
  openModal('updateModal');
}

function openDeleteModal(id, name) {
  document.getElementById('deleteStudentName').innerText = `Delete "${name}"?`;
  const btn = document.getElementById('confirmDeleteBtn');
  btn.onclick = async function () {
    const response = await fetch(`/admin/delete-student/${id}`, { method: 'DELETE' });
    if (response.ok) location.reload();
    else alert('Failed to delete student.');
  };
  openModal('deleteModal');
}

// Add student
document.getElementById('addForm').onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const res = await fetch('/admin/add-student', { method: 'POST', body: formData });
  if (res.ok) location.reload();
  else alert('Failed to add student.');
};

// Update student
document.getElementById('updateForm').onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const res = await fetch('/admin/update-student', { method: 'POST', body: formData });
  if (res.ok) location.reload();
  else alert('Failed to update student.');
};
