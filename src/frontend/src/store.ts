import { ref, shallowRef } from "vue";

import ClientAPI from "@/api";
import { defineStore } from "pinia";
import qs from "qs";

interface optionsParam {
    from: string|null;
    to: string|null;
    unique?: number;
    owc?: number
}
const qsStringifyOptions: qs.IStringifyOptions = { addQueryPrefix: true, skipNulls: true, arrayFormat: "repeat" };
const stringifyParams = ({ from, to, ...other }: optionsParam) => qs.stringify({ from, to, ...other }, qsStringifyOptions);

export const useApplicationStore = defineStore("app_store", () => {
    /** http клиент */
    const api = new ClientAPI();

    const tasks = shallowRef<Array<frontend.ITaskL>>([]);
    const positions = ref<Array<frontend.ITaskPosition>>([]);

    const fetchTasksList = () => api.fetchTasksList().then(body => tasks.value = body);
    const fetchTaskPositions = (taskID: number) => api.fetchTaskPositions(taskID).then(body => positions.value = body);

    return {
        fetchTasksList,
        fetchTaskPositions,
        tasks,
        positions
    };
});
