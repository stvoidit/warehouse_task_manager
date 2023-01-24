import jwt_decode from "jwt-decode";

const BASE_URL = "/api";
const TASKS_LIST = "tasks";
const TASK_POSITIONS = "task";
const LOGIN = "login";


type user = {
    can_login: number;
    id: string;
    employee_name: string;
    login: string;
}

class ClientAPI {
    currentUser: user | null = null;
    token: string | null;
    constructor() {
        this.currentUser = null;
        this.token = "";
    }

    decodeToken() {
        /** декодирование токена */
        if (this.token) {
            const decode_token = jwt_decode(this.token);
            this.currentUser = decode_token ? decode_token["payload"] : null;
        }
    }

    checkToken() {
        /** проверка токена */
        if (location.pathname === "/login") return;
        if (!this.token) {
            this.token = window.localStorage.getItem("token");
        }
        if (!this.token) {
            location.href = "/login";
        }
        if (!this.currentUser) {
            this.decodeToken();
        }
    }

    requestHeaders() {
        return this.token ? { token: this.token } : {};
    }

    async fetchTasksList() {
        /** получение списка задач */
        this.checkToken();
        const response = await fetch(`${BASE_URL}/${TASKS_LIST}`, { headers: this.requestHeaders() });
        if (response.status === 403) {
            window.localStorage.removeItem("token");
            location.href = "/login";
        }
        const body = await response.json();
        return body;
    }

    async fetchTaskPositions(taskID: number) {
        /** получение списка позиций в задаче */
        this.checkToken();
        const response = await fetch(`${BASE_URL}/${TASK_POSITIONS}/${taskID}`, { headers: this.requestHeaders() });
        if (response.status === 403) {
            window.localStorage.removeItem("token");
            location.href = "/login";
        }
        if (response.status !== 200) {
            location.href = "/";
            return;
        }
        const body = await response.json();
        return body;
    }

    async doLogin(payload: frontend.ILoginPayload) {
        /** авторизация */
        const response = await fetch(`${BASE_URL}/${LOGIN}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
        if (response.ok === false) {
            throw "Неправильный логин или пароль";
        }
        const token = await response.json();
        window.localStorage.setItem("token", token);
        this.decodeToken();
        location.href = "/";
        return;
    }
}

export default ClientAPI;
