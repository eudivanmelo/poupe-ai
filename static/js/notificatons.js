const notifications = [
    { id: 1, title: "Nova mensagem", message: "Você tem uma nova mensagem.", read: false, created_at: "2025-01-14T09:00:00Z" },
    { id: 2, title: "Atualização", message: "Seu pedido foi enviado.", read: true, created_at: "2025-01-13T15:00:00Z" },
    { id: 3, title: "Promoção", message: "Aproveite nossa promoção especial!", read: false, created_at: "2025-01-14T08:30:00Z" },
    { id: 4, title: "Aviso", message: "Atualize sua senha para maior segurança.", read: true, created_at: "2025-01-12T12:00:00Z" },
];

const notificationsContainer = document.getElementById("notifications");
const notificationDetails = document.getElementById("notification-details");

function timeAgo(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - new Date(date)) / 1000);

    const minutes = Math.floor(diffInSeconds / 60);
    const hours = Math.floor(diffInSeconds / 3600);
    const days = Math.floor(diffInSeconds / 86400);

    if (days > 0) {
        return `${days} dia(s) atrás`;
    } else if (hours > 0) {
        return `${hours} hora(s) atrás`;
    } else if (minutes > 0) {
        return `${minutes} minuto(s) atrás`;
    } else {
        return "Agora mesmo";
    }
}

function renderNotifications() {
    notificationsContainer.innerHTML = "";
    notifications.forEach((notification) => {
        const li = document.createElement("li");
        li.className = `list-group-item d-flex justify-content-between align-items-center notification-item ${notification.read ? "" : "unread"}`;
        li.innerHTML = `
            <span>${notification.title}</span>
            <small class="text-muted">${timeAgo(notification.created_at)}</small>
            <div class="btn-group">
                <button class="btn btn-sm btn-outline-success" onclick="markAsRead(${notification.id})">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteNotification(${notification.id})">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        `;
        li.onclick = () => showNotificationDetails(notification);
        notificationsContainer.appendChild(li);
    });
}

function showNotificationDetails(notification) {
    notificationDetails.innerHTML = `
        <h5 class="text-primary">${notification.title}</h5>
        <p>${notification.message}</p>
        <small class="text-muted">Enviada ${timeAgo(notification.created_at)}</small>
    `;
}

function markAsRead(id) {
    const notification = notifications.find((n) => n.id === id);
    if (notification) {
        notification.read = true;
        renderNotifications();
    }
}

function deleteNotification(id) {
    const index = notifications.findIndex((n) => n.id === id);
    if (index !== -1) {
        notifications.splice(index, 1);
        renderNotifications();
        notificationDetails.innerHTML = `
            <p class="empty-details">Selecione uma notificação para visualizar os detalhes.</p>
        `;
    }
}

renderNotifications();