async function fetchCharacters() {
    const response = await fetch("/characters");
    const data = await response.json();
    const table = document.getElementById("character-table");
    if (!table) return; // Voorkom errors als de tabel niet bestaat
    table.innerHTML = "";
    data.forEach((char, index) => {
        table.innerHTML += `<tr>
            <td>${char.name}</td>
            <td>${char.type}</td>
            <td>${char.path}</td>
            <td>
                <button onclick="editCharacter(${index}, '${char.name}', '${char.type}', '${char.path}')">Edit</button>
                <button onclick="deleteCharacter(${index})">Delete</button>
            </td>
        </tr>`;
    });
}

async function addCharacter() {
    const name = document.getElementById("name").value;
    const type = document.getElementById("type").value;
    const path = document.getElementById("path").value;

    const response = await fetch("/characters", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, type, path })
    });

    if (response.ok) {
        location.reload();
    } else {
        console.error("Failed to add character:", await response.json());
    }
}

async function deleteCharacter(index) {
    if (confirm("Are you sure you want to delete this character?")) {
        const response = await fetch(`/characters/${index}`, { method: "DELETE" });
        if (response.ok) {
            location.reload();
        } else {
            alert("Failed to delete character.");
        }
    }
}

function editCharacter(index, name, type, path) {
    const newName = prompt("Enter new name:", name) || name;
    const newType = prompt("Enter new element:", type) || type;
    const newPath = prompt("Enter new path:", path) || path;
    
    fetch(`/characters/${index}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName, type: newType, path: newPath })
    }).then(response => {
        if (response.ok) location.reload();
        else alert("Failed to update character.");
    });
}

fetchCharacters();