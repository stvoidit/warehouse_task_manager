import { computed, reactive, ref, shallowRef } from "vue";

import ClientAPI from "@/api";
import { defineStore } from "pinia";

export default defineStore("app_store", () => {
    /** http клиент */
    const api = reactive(new ClientAPI());
    /** флаг процесса загрузки данных */
    const loading = ref(false);
    /** информация из декодированного токена о пользователе */
    const currentUser = computed(() => api.currentUser);
    /** вычисляемое свойство - авторизован пользователь или нет */
    const isAuth = computed(() => currentUser.value?.can_login === 1);
    /** проверка токена клиента внутри браузера */
    const checkToken = () => api.checkToken();

    /** список складов */
    const stocks = shallowRef<Array<frontend.IStock>>([]);
    /** список заданий */
    const tasks = shallowRef<Array<frontend.ITaskL>>([]);
    /** список прогресса заданий */
    const tasks_progress = shallowRef<Array<frontend.ITaskL>>([]);
    /** задание */
    const task = ref<frontend.ITaskP | null>(null);


    const doLogin = (payload: frontend.ILoginPayload) => api.doLogin(payload);
    /** запрос к API для получения списка складов */
    const fetchStocks = () => {
        return api.fetchStocks().then(body => stocks.value = body).finally(() => loading.value = false);
    };
    /** запрос к API для получения списка задач */
    /** запрос к API для получения списка прогрессса по задачам */
    const fetchTasksList = (stockID: number) => {
        loading.value = true;
        return Promise.all([
            api.fetchTasksList(stockID).then(body => tasks.value = body),
            api.fetchTasksProgress(stockID).then(body => tasks_progress.value = body)
        ]).finally(() => loading.value = false);
        return api.fetchTasksList(stockID).then(body => tasks.value = body).finally(() => loading.value = false);
    };

    /** запрос к API для получения данных задания */
    const fetchTask = (stockID: number, taskID: number, materialID: number, tareType: string, with_load=true) => {
        if (with_load) loading.value = true;
        return api.fetchTask(stockID, taskID, materialID, tareType).then(body => task.value = body).finally(() => {
            if (with_load) loading.value = false;
        });
    };
    /** запрос к API на изменение пароля */
    const changePassword = (payload: frontend.IChangePassword) => {
        loading.value = true;
        return api.changePasswor(payload).finally(() => loading.value = false);
    };
    /** изменение статуса "выполнено" для задания в задаче */
    const updateJobStatus = (taskID: number, materialID: number, taraID: number, netWeightFact: number, add_processing_id: number, done: boolean) => {
        return api.updateJobStatus(taskID, materialID, taraID, netWeightFact, add_processing_id, done);
    };

    /** ID таймера */
    let timer: NodeJS.Timer;
    /** интервал в ms для setInterval */
    const delay = 15_000;
    /** запуск автообновления */
    const doAutofetch = (stockID: number, taskID: number, materialID: number, tareType: string) => {
        timer = setInterval(() => {
            fetchTask(stockID, taskID, materialID, tareType, false);
        }, delay);
    };
    /** остановка автообновления */
    const stopAutofetch = () => {
        clearInterval(timer);
    };

    /** т.к. процесс выхода (logout) не требует фиксации на бэке, то достаточно просто стереть токен из памяти */
    const logOut = () => {
        api.currentUser = null;
        api.token = null;
        window.localStorage.removeItem("token");
        location.href = "/login";
    };

    const orientation = ref("landscape-primary");
    const isLandscape = computed(() => orientation.value === "landscape-primary");
    try {
        orientation.value = screen.orientation.type;
        window.addEventListener("orientationchange", () => {
            orientation.value = screen.orientation.type;
        }, false);
    } catch (error) {
        // eslint-disable-next-line
        console.warn(error);
    }


    return {
        doLogin,
        fetchStocks,
        fetchTasksList,
        fetchTask,
        updateJobStatus,
        stocks,
        tasks,
        tasks_progress,
        task,
        isAuth,
        currentUser,
        checkToken,
        changePassword,
        logOut,
        loading,
        isLandscape,

        doAutofetch,
        stopAutofetch
    };
});
