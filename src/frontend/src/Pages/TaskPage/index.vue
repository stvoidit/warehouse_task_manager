<template>
    <el-row v-loading="store.loading">
        <el-col v-if="store.task">
            <MetaInfo
                :meta-info="metaInfo"
                :doc-number="store.task.doc_number"
                :material="store.task.material">
                <FiltersJobs
                    v-model:selected-statuses="selectedStatuses"
                    v-model:selected-categorits="selectedCategorits"
                    :categories-options="categoriesOptions" />
            </MetaInfo>
            <StatInfo :stat-info="statInfo" />
            <JobsTable
                :jobs-list="computedJobsData"
                @change-status="updateJobStatus" />
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, ref } from "vue";
import { useRouter } from "vue-router";
import useApplicationStore from "@/store";
import { ElMessage, ElMessageBox } from "element-plus";
import dayjs from "dayjs";
import MetaInfo from "./MetaInfo.vue";
import StatInfo from "./StatInfo.vue";
import FiltersJobs from "./FiltersJobs.vue";
import JobsTable from "./JobsTable.vue";

const props = defineProps({
    /** ID склада */
    stockID: { type: Number, required: true },
    /** ID задачи */
    taskID: { type: Number, required: true },
    /** ID материала */
    materialID: { type: Number, required: true }
});
const router = useRouter();
const store = useApplicationStore();
const searchParams = new URLSearchParams(location.search);
const queryParams = {
    /** Тип тары */
    tareType: searchParams.get("tareType") ?? "",
    /** Категория материала в задаче */
    categoryTask: searchParams.get("categoryTask")??""
};
/**
 * 1) Получение данных задачи
 * 2) Запуск автообновления
 */
onMounted(() => {
    if (isNaN(props.taskID)) router.push("/");
    store.fetchTask(props.stockID, props.taskID, props.materialID, queryParams.tareType);
    store.doAutofetch(props.stockID, props.taskID, props.materialID, queryParams.tareType);
});
/**
 * Остановка автообновления
 */
onBeforeUnmount(() => {
    store.task = null;
    store.stopAutofetch();
});
/** Запрос к API на обновление статуса задания */
const updateJobStatus = async (job: frontend.IJob) => {
    try {
        const newStatus = !job.done;
        if (newStatus === true && job.task_net_weight > remainingWeight.value[job.category]) {
            try {
                await ElMessageBox.confirm(
                    `Превышение веса на ${(remainingWeight.value[job.category]-job.task_net_weight)*-1}`,
                    "Предупреждение",
                    {
                        confirmButtonText: "Подтверждение",
                        cancelButtonText: "Отмена",
                        type: "warning"
                    }
                );
            } catch (error) {
                console.warn(error);
                return;
            }
        }
        await store.updateJobStatus(props.taskID, props.materialID, job.tare_id, newStatus);
        await store.fetchTask(props.stockID, props.taskID, props.materialID, queryParams.tareType);
        const readebleStatus = newStatus === true ? "готово" : "не выполнено";
        const message = `Тара с маркировкой "${job.tare_mark}" (тара ${job.tare_id}) - статус изменен на "${readebleStatus}"`;
        ElMessage({
            showClose: false,
            message: message,
            type: newStatus ? "success" : "warning"
        });
    } catch (error) {
        alert(error);
    }
};
/** Функция для подсчета кол-ва заданий по статусу */
const sumJobsStatus = (jobs: Array<frontend.IJob>, status: boolean, category: string) => {
    return jobs.reduce((prev, job) => prev = job.done === status && job.category === category ? prev + 1 : prev, 0);
};
/** Вычисляемое свойство (обертка для таблицы) - метаданные задачи */
const metaInfo = computed(() => ({
    fields: [
        {
            label: "Материал",
            prop: "material"
        },
        {
            label: "Техпроцесс",
            prop: "technical_process"
        },
        {
            label: "Операция",
            prop: "operation"
        },
        {
            label: "Тара",
            prop: "tareType"
        },
        {
            label: "Плановая дата",
            prop: "planned_date"
        }
    ],
    data: [
        {
            material: store.task?.material,
            technical_process: store.task?.technical_process,
            operation: store.task?.operation,
            tareType: queryParams.tareType,
            planned_date: dayjs(store.task?.planned_date, "YYYY-MM-DD").format("DD.MM.YYYY")
        }
    ]
}));

/** Вычисляемое свойство (обертка для таблицы) - статистика заданий */
const statInfo = computed(() => {
    const findTaskWeight = (category: string) => {
        const catWeightstore = store.task?.task_weights.find(tw => tw.category === category);
        if (catWeightstore) {
            return catWeightstore.task_weight;
        }
        return store.task?.jobs.reduce((prev,cur) => cur.category === category ? prev+=cur.task_net_weight : prev, 0)??0;
    };
    const sumNetWeightComplited = (category: string) => {
        return store.task?.jobs.reduce((prev,cur) => cur.done && cur.category === category ? prev+=cur.task_net_weight : prev, 0)??0;
    };
    return categoriesOptions.value.map(category => ({
        categoryLabel: category,
        data: [
            {
                label: "Заданий",
                count: store.task?.jobs.reduce((prev,cur) => cur.category === category ? prev+=1 : prev, 0),
                netWeight: findTaskWeight(category)
            },
            {
                label: "Выполнено",
                count: store.task?.jobs ? sumJobsStatus(store.task.jobs, true, category) : 0,
                netWeight: store.task?.jobs.reduce((prev,cur) => cur.done && cur.category === category ? prev+=cur.task_net_weight : prev, 0)
            },
            {
                label: "Осталось",
                count: store.task?.jobs ? sumJobsStatus(store.task.jobs, false, category) : 0,
                netWeight: findTaskWeight(category) - sumNetWeightComplited(category)
            }
        ]
    }));
});

/** Остатки веса по категориям */
const remainingWeight = computed(() => {
    const remainings: {[key: string]: number} = {};
    statInfo.value.forEach(si => {
        remainings[si.categoryLabel] = si.data[2]?.netWeight??0;
    });
    return remainings;
});

/** фильтр по статусам */
const selectedStatuses = ref<number>(0);
/** фильтр по категории */
const selectedCategorits = ref<string[]>([]);
const categoriesOptions = computed(() => Array.from(new Set<string>(store.task?.jobs.map(job => job.category === "" ? "" : job.category))).sort());
/** Список работ для таблицы с учетом фильтров */
const computedJobsData = computed<frontend.IJob[]>(() => {
    let jobs = (store.task?.jobs ?? []).filter(j => {
        switch (selectedStatuses.value) {
        case 1:
            return j.done === true;
        case 2:
            return j.done === false;
        default:
            return true;
        }
    });
    return selectedCategorits.value.length ? jobs.filter(j => selectedCategorits.value.includes(j.category)) : jobs;
});
</script>
