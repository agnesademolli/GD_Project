document.addEventListener("DOMContentLoaded", () => {
    const serviceList = document.getElementById("service-list");
    const serviceForm = document.getElementById("service-form");

    // Fetch and display all services
    function fetchServices() {
        fetch("/api/services")
            .then(response => response.json())
            .then(data => {
                serviceList.innerHTML = data.map(service => `
                    <li id="service-${service.id}">
                        <strong>${service.name}</strong>: ${service.description}
                        <button onclick="deleteService(${service.id})">Delete</button>
                        <button onclick="editService(${service.id}, '${service.name}', '${service.description}')">Edit</button>
                    </li>
                `).join("");
            });
    }

    // Create a new service
    serviceForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(serviceForm);
        const name = formData.get("name");
        const description = formData.get("description");

        fetch("/api/services", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        }).then(() => {
            fetchServices();
            serviceForm.reset();
        });
    });

    // Delete a service
    window.deleteService = (id) => {
        fetch(`/api/services/${id}`, { method: "DELETE" })
            .then(() => fetchServices());
    };

    // Edit a service
    window.editService = (id, name, description) => {
        const newName = prompt("Edit Name:", name);
        const newDescription = prompt("Edit Description:", description);

        if (newName && newDescription) {
            fetch(`/api/services/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: newName, description: newDescription })
            }).then(() => fetchServices());
        }
    };

    // Initial fetch
    fetchServices();
});
