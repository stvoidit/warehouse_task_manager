const BASE_URL = "/api";
const TASKS_LIST = "tasks";
const TASK_POSITIONS = "task";


type user = {
    canLogin: boolean;
    id: string;
    name: string;
    position: string;
    sessionID: string;
}

class ClientAPI {
    currentUser: user | null = null;
    constructor() {
        this.currentUser = null;
    }

    async fetchTasksList() {
        const response = await fetch(`${BASE_URL}/${TASKS_LIST}`);
        const body = await response.json();
        return body;
    }

    async fetchTaskPositions(taskID: number) {
        const response = await fetch(`${BASE_URL}/${TASK_POSITIONS}/${taskID}`);
        if (response.status !== 200) {
            location.href = "/";
            return;
        }
        const body = await response.json();
        return body;
    }
}

export default ClientAPI;
