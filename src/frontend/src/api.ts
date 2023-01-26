import jwt_decode from "jwt-decode";

const BASE_URL = "/api";
const TASKS_LIST = "tasks";
const TASK_POSITIONS = "task";
const LOGIN = "login";
const CHANGE_PASSWORD = "change_password";


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

    requestHeaders(): HeadersInit {
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

    async fetchTask(taskID: number): Promise<frontend.ITaskP> {
        /** получение списка позиций в задаче */
        this.checkToken();
        const response = await fetch(`${BASE_URL}/${TASK_POSITIONS}/${taskID}`, { headers: this.requestHeaders() });
        if (response.status === 403) {
            window.localStorage.removeItem("token");
            location.href = "/login";
        }
        if (response.status !== 200) {
            location.href = "/";
        }
        const body = await response.json();
        body.jobs.forEach(job => job.done = Boolean(job.done));
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

    async changePasswor(payload: frontend.IChangePassword) {
        const response = await fetch(`${BASE_URL}/${CHANGE_PASSWORD}`, { method: "POST", headers: { "Content-Type": "application/json", ...this.requestHeaders() }, body: JSON.stringify(payload) });
        if (response.status !== 201) {
            throw new Error(await response.text());
        }
        return;
    }
}

export default ClientAPI;
