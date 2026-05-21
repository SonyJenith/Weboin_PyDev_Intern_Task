// API Configuration
const API_BASE = "http://localhost:8000"; // Backend API URL

// State Management
let currentPage = 1;
let currentFilter = "all";
let authToken = localStorage.getItem("token");
let currentUsername = localStorage.getItem("username");

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
    if (authToken) {
        showSection("tasks");
        document.getElementById("username").textContent = currentUsername;
        setUserAvatar(currentUsername);
        fetchTasks();
    } else {
        showSection("auth");
    }
    
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Auth forms
    document.getElementById("register-form").addEventListener("submit", handleRegister);
    document.getElementById("login-form").addEventListener("submit", handleLogin);
    
    // Tasks
    document.getElementById("create-task-form").addEventListener("submit", handleCreateTask);
    document.getElementById("logout-btn").addEventListener("click", handleLogout);
    
    // Filter buttons
    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", handleFilterChange);
    });
    
    // Pagination
    document.getElementById("prev-btn").addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            fetchTasks();
        }
    });
    
    document.getElementById("next-btn").addEventListener("click", () => {
        currentPage++;
        fetchTasks();
    });
}

// Set user avatar with first letter
function setUserAvatar(username) {
    const avatar = document.getElementById("user-avatar");
    if (avatar && username) {
        avatar.textContent = username.charAt(0).toUpperCase();
    }
}

// Auth Functions
async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password }),
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Registration failed");
        }
        
        showError("register-error", "");
        document.getElementById("register-form").reset();
        alert("Registration successful! Please log in with your credentials.");
        toggleAuthForm();
    } catch (error) {
        showError("register-error", error.message);
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Login failed");
        }
        
        const data = await response.json();
        authToken = data.access_token;
        currentUsername = username;
        
        localStorage.setItem("token", authToken);
        localStorage.setItem("username", currentUsername);
        
        showError("login-error", "");
        document.getElementById("login-form").reset();
        showSection("tasks");
        document.getElementById("username").textContent = currentUsername;
        setUserAvatar(currentUsername);
        currentPage = 1;
        currentFilter = "all";
        fetchTasks();
    } catch (error) {
        showError("login-error", error.message);
    }
}

function handleLogout() {
    authToken = null;
    currentUsername = null;
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    
    document.getElementById("register-form").reset();
    document.getElementById("login-form").reset();
    document.getElementById("create-task-form").reset();
    
    currentPage = 1;
    currentFilter = "all";
    
    // Reset filter buttons
    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.classList.remove("active");
        if (btn.dataset.filter === "all") {
            btn.classList.add("active");
        }
    });
    
    // Show register form
    document.getElementById("register-form-container").style.display = "block";
    document.getElementById("login-form-container").style.display = "none";
    
    showSection("auth");
}

// Task Functions
async function handleCreateTask(e) {
    e.preventDefault();
    const title = document.getElementById("task-title").value;
    const description = document.getElementById("task-description").value;
    
    try {
        const response = await fetch(`${API_BASE}/tasks/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`,
            },
            body: JSON.stringify({ title, description: description || null }),
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Failed to create task");
        }
        
        showError("create-task-error", "");
        document.getElementById("create-task-form").reset();
        currentPage = 1;
        fetchTasks();
    } catch (error) {
        showError("create-task-error", error.message);
    }
}

async function fetchTasks() {
    try {
        let url = `${API_BASE}/tasks/?page=${currentPage}&page_size=10`;
        
        if (currentFilter === "completed") {
            url += "&completed=true";
        } else if (currentFilter === "pending") {
            url += "&completed=false";
        }
        
        const response = await fetch(url, {
            headers: { "Authorization": `Bearer ${authToken}` },
        });
        
        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }
        
        const data = await response.json();
        renderTasks(data);
        updatePagination(data);
    } catch (error) {
        console.error(error);
    }
}

function renderTasks(data) {
    const tasksList = document.getElementById("tasks-list");
    
    if (!data.tasks || data.tasks.length === 0) {
        tasksList.innerHTML = '<div class="empty-state"><div class="empty-state-icon">→</div><p>No tasks yet. Create your first task to get started.</p></div>';
        return;
    }
    
    tasksList.innerHTML = data.tasks.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}">
            <div class="task-content">
                <div class="task-header">
                    <div>
                        <h3 class="task-title ${task.completed ? 'completed' : ''}">${escapeHtml(task.title)}</h3>
                        ${task.description ? `<p class="task-description">${escapeHtml(task.description)}</p>` : ''}
                    </div>
                    <span class="status-badge ${task.completed ? 'completed' : 'pending'}">
                        ${task.completed ? 'Completed' : 'Pending'}
                    </span>
                </div>
            </div>
            <div class="task-actions">
                ${!task.completed ? `<button class="btn btn-complete btn-small" onclick="markTaskComplete(${task.id})">Complete</button>` : ''}
                <button class="btn btn-delete btn-small" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function markTaskComplete(taskId) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`,
            },
            body: JSON.stringify({ completed: true }),
        });
        
        if (!response.ok) {
            throw new Error("Failed to update task");
        }
        
        fetchTasks();
    } catch (error) {
        console.error(error);
        alert("Failed to update task");
    }
}

async function deleteTask(taskId) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${authToken}` },
        });
        
        if (!response.ok) {
            throw new Error("Failed to delete task");
        }
        
        fetchTasks();
    } catch (error) {
        console.error(error);
        alert("Failed to delete task");
    }
}

// Filter functions
function handleFilterChange(e) {
    document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));
    e.target.classList.add("active");
    
    currentFilter = e.target.dataset.filter;
    currentPage = 1;
    fetchTasks();
}

// Pagination update
function updatePagination(data) {
    document.getElementById("page-label").textContent = `Page ${data.page}`;
    document.getElementById("prev-btn").disabled = data.page === 1;
    document.getElementById("next-btn").disabled = data.total <= data.page * data.page_size;
}

// UI Helper functions
function showSection(section) {
    document.getElementById("auth-section").style.display = section === "auth" ? "flex" : "none";
    document.getElementById("tasks-section").style.display = section === "tasks" ? "block" : "none";
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (message) {
        errorElement.textContent = message;
        errorElement.classList.add("show");
    } else {
        errorElement.textContent = "";
        errorElement.classList.remove("show");
    }
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
