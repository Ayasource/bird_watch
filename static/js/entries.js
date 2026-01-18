const editButtons = document.getElementsByClassName("btn-edit");
const entryText = document.getElementsById("id_body");
const entryForm = document.getElementsById("entryForm");
const submitButton = document.getElementsById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
Initializes edit functionality for the provided edit buttons.

For each button in the `editButtons` collection:
- Retrieves the associated entry's ID upon click.
- Fetches the content of the corresponding entry.
- Populates the `entryText` input/textarea with the entry's content for editing.
- Updates the submit button's text to "Update".
- Sets the form's action attribute to the `edit_entry/{editId}` endpoint.
*/
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
     let entryId = e.target.getAttribute("entry_id");
     let entryContent = document.getElementById(`entry${entryId}`).innerText; 
     entryText.value = entryContent;
     submitButton.innerText = "Update";
     entryForm.setAttribute("action", `edit_entry/${entryId}`);
  });
}
/**
Initializes deletion functionality for the provided delete buttons.

For each button in the `deletetButtons` collection:
- Retrieves the associated entry's ID upon click.
- Updates the `deleteConfirm` link's href to point to the deletion endpoint for the specific comment.
- Displays a confirmation modal (`deleteModel`) to prompt the user for confirmation before deletion.
*/

for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
     let entryId = e.target.getAttribute("entry_id");
     deleteConfirm.href = `delete_comment/${entryId}`;
     deleteModal.show(); 
  });
}
         

