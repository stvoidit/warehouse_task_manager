<template>
    <el-row v-if="store.isAuth">
        <el-col v-loading="store.loading">
            <el-row class="mb sticky-row">
                <el-col>
                    <span style="font-size: 1.4em;"><b>{{ store.task?.doc_number }}{{ store.task?.material ? ` - ${store.task?.material}` : '' }}</b></span>
                    <el-table
                        class="mt"
                        :data="metaInfo.data"
                        :border="true"
                        :fit="false"
                        :show-header="true"
                        table-layout="fixed">
                        <el-table-column
                            v-for="field in metaInfo.fields"
                            :key="field.prop"
                            :prop="field.prop"
                            :label="field.label"
                            :width="150" />
                    </el-table>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col
                    v-for="cat in statInfo"
                    :key="cat.categoryLabel"
                    class="mb"
                    :xs="24"
                    :sm="12"
                    :md="12"
                    :lg="8"
                    :xl="6">
                    <div :style="{minHeight: '1.3rem'}">
                        <b>{{ cat.categoryLabel }}</b>
                    </div>
                    <el-table
                        :data="cat.data"
                        :border="true"
                        :show-header="false"
                        table-layout="auto">
                        <el-table-column
                            prop="label"
                            :width="150" />
                        <el-table-column
                            prop="count" />
                        <el-table-column
                            prop="netWeight" />
                    </el-table>
                </el-col>
            </el-row>
            <el-row
                class="mb sticky-row top-padding"
                :gutter="10">
                <el-col
                    :xs="12"
                    :sm="8"
                    :md="6"
                    :lg="3"
                    :xl="3">
                    <span><small>Фильтр по статусу выполнения</small></span>
                    <el-select
                        v-model="selectedStatuses"
                        placeholder="Статус">
                        <el-option
                            v-for="item in statusesOptions"
                            :key="item.label"
                            :label="item.label"
                            :value="item.value" />
                    </el-select>
                </el-col>
                <el-col
                    v-if="categoriesOptions.length>1"
                    :xs="12"
                    :sm="8"
                    :md="6"
                    :lg="3"
                    :xl="3">
                    <span><small>Фильтр по статусу выполнения</small></span>
                    <el-select
                        v-model="selectedCategorits"
                        multiple
                        clearable
                        placeholder="Категории">
                        <el-option
                            v-for="item in categoriesOptions"
                            :key="item"
                            :label="item"
                            :value="item" />
                    </el-select>
                </el-col>
            </el-row>
            <el-row class="mb">
                <el-col>
                    <el-table
                        :data="computedJobsData"
                        :border="true"
                        @row-click="handleClickRow">
                        <el-table-column
                            width="130"
                            prop="done"
                            column-key="done"
                            label="Выполнено">
                            <template #default="scope">
                                <div style="text-align: center;">
                                    <el-checkbox
                                        v-model="scope.row.done"
                                        size="large"
                                        @change="updateJobStatus(scope.row.tare_id, scope.row.done, scope.row.tare_mark)" />
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column
                            v-for="col in columns"
                            :key="col.prop"
                            :prop="col.prop"
                            :column-key="col.prop"
                            :label="col.label"
                            :min-width="col.width" />
                    </el-table>
                </el-col>
            </el-row>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useApplicationStore } from "@/store";
import { ElMessage } from "element-plus";
import dayjs from "dayjs";

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
const updateJobStatus = async (tare_id: number, done: boolean, tare_mark: string) => {
    try {
        await store.updateJobStatus(props.taskID, props.materialID, tare_id, done);
        await store.fetchTask(props.stockID, props.taskID, props.materialID, queryParams.tareType);
        const readebleStatus = done === true ? "готово" : "не выполнено";
        const message = `Тара с маркировкой "${tare_mark}" (тара ${tare_id}) - статус изменен на "${readebleStatus}"`;
        ElMessage({
            showClose: false,
            message: message,
            type: done ? "success" : "warning"
        });
    } catch (error) {
        alert(error);
    }
};
/** Обработчик клика на строку - запрос на обновление статуса задания */
const handleClickRow = (row: frontend.IJob, column: any) => {
    if (column.no === 0) return;
    updateJobStatus(row.tare_id, !row.done, row.tare_mark);
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

/** фильтр по статусам */
const selectedStatuses = ref<boolean | string>("all");
const statusesOptions = [
    {
        label: "Все",
        value: "all"
    },
    {
        label: "Выполнено",
        value: true
    },
    {
        label: "Не выполнено",
        value: false
    }
];
/** фильтр по категории */
const selectedCategorits = ref<string[]>([]);
const categoriesOptions = computed(() => Array.from(new Set<string>(store.task?.jobs.map(job => job.category === "" ? "" : job.category))).sort());
/** Список работ для таблицы с учетом фильтров */
const computedJobsData = computed<frontend.IJob[]>(() => {
    let jobs = (store.task?.jobs ?? []).filter(j => {
        switch (selectedStatuses.value) {
        case true:
            return j.done === true;
        case false:
            return j.done === false;
        default:
            return true;
        }
    });
    return selectedCategorits.value.length ? jobs.filter(j => selectedCategorits.value.includes(j.category)) : jobs;
});

/** Вычисляемое свойство (обертка для таблицы) - статистика заданий */
const statInfo = computed(() => {
    return categoriesOptions.value.map(c => ({
        categoryLabel: c,
        data: [
            {
                label: "Заданий",
                count: store.task?.jobs.reduce((prev,cur) => cur.category === c ? prev+=1 : prev, 0),
                netWeight: store.task?.jobs.reduce((prev,cur) => cur.category === c ? prev+=cur.task_net_weight : prev, 0)
            },
            {
                label: "Выполнено",
                count: store.task?.jobs ? sumJobsStatus(store.task.jobs, true, c) : 0,
                netWeight: store.task?.jobs.reduce((prev,cur) => cur.done && cur.category === c ? prev+=cur.task_net_weight : prev, 0)
            },
            {
                label: "Осталось",
                count: store.task?.jobs ? sumJobsStatus(store.task.jobs, false, c) : 0,
                netWeight: store.task?.jobs.reduce((prev,cur) => !cur.done && cur.category === c ? prev+=cur.task_net_weight : prev, 0)
            }
        ]
    }));
});
/** Список столбцов таблицы */
const columns = [
    {
        prop: "tare_id",
        label: "Номер",
        width: 100,
        sortable: false
    },
    {
        prop: "tare_mark",
        label: "Маркировка",
        width: 150,
        sortable: false
    },
    {
        prop: "tare_type",
        label: "Тара",
        width: 100,
        sortable: false
    },
    {
        prop: "category",
        label: "Категория",
        width: 150,
        sortable: true
    },
    {
        prop: "rest_gross_weight",
        label: "Брутто",
        width: 150,
        sortable: false
    },
    {
        prop: "task_net_weight",
        label: "Нетто",
        width: 150,
        sortable: false
    }
];

// /** Подсветка строк по статусе */
// const rowClassName = ({ row }: { row: frontend.IJob }) => {
//     if (statInfo.value.length < 2) return "";
//     if (row.category === queryParams.categoryTask && !row.done) {
//         return "category-row";
//     }
//     if (row.done) {
//         return "row-done";
//     }
//     return "";
// };
// const filterHandler = (value: string, row: frontend.IJob) => {
//     const isDone = value === "true" ? true : false;
//     return row.done === isDone;
// };
</script>
