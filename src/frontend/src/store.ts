import { computed, reactive, ref, shallowRef } from "vue";

import ClientAPI from "@/api";
import { defineStore } from "pinia";

export default defineStore("app_store", () => {
    /** http клиент */
    const api = reactive(new ClientAPI());
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
    /** задание */
    const task = ref<frontend.ITaskP | null>(null);
    /** флаг процесса загрузки данных */
    const loading = ref(false);

    const doLogin = (payload: frontend.ILoginPayload) => api.doLogin(payload);
    /** запрос к API для получения списка складов */
    const fetchStocks = () => {
        return api.fetchStocks().then(body => stocks.value = body).finally(() => loading.value = false);
    };
    /** запрос к API для получения списка задач */
    const fetchTasksList = (stockID: number) => {
        loading.value = true;
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
    const autofetchEnabled = ref(false);
    /** интервал в ms для setInterval */
    const delay = 15_000;
    /** запуск автообновления */
    const doAutofetch = (stockID: number, taskID: number, materialID: number, tareType: string) => {
        timer = setInterval(() => {
            fetchTask(stockID, taskID, materialID, tareType, false);
        }, delay);
        autofetchEnabled.value = true;
    };
    /** остановка автообновления */
    const stopAutofetch = () => {
        clearInterval(timer);
        autofetchEnabled.value = false;
    };

    /** т.к. процесс выхода (logout) не требует фиксации на бэке, то достаточно просто стереть токен из памяти */
    const logOut = () => {
        api.currentUser = null;
        api.token = null;
        window.localStorage.removeItem("token");
        location.href = "/login";
    };

    return {
        doLogin,
        fetchStocks,
        fetchTasksList,
        fetchTask,
        updateJobStatus,
        stocks,
        tasks,
        task,
        isAuth,
        currentUser,
        checkToken,
        changePassword,
        logOut,
        loading,

        doAutofetch,
        stopAutofetch,
        autofetchEnabled
    };
});
