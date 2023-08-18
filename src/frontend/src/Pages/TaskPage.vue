<template>
    <el-row v-if="store.isAuth">
        <el-col v-loading="store.loading">
            <el-row class="mb sticky-row">
                <el-col>
                    <span><b>{{ store.task?.doc_number }}{{ queryParams.categoryTask ? ` - ${queryParams.categoryTask}` : '' }}</b></span>
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
            <el-row
                class="mb"
                :gutter="20">
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
            <el-row>
                <el-col>
                    <el-table
                        :data="store.task?.jobs"
                        :border="true"
                        :row-class-name="rowClassName"
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
import { onMounted, onBeforeUnmount, computed } from "vue";
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
const sumJobsStatus = (jobs: Array<frontend.IJob>, status: boolean) => jobs.reduce((prev, job) => prev = job.done === status ? prev + 1 : prev, 0);
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
            label: "Категория",
            prop: "categoryTask"
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
            categoryTask: queryParams.categoryTask,
            planned_date: dayjs(store.task?.planned_date, "YYYY-MM-DD").format("DD.MM.YYYY")
        }
    ]
}));

/** Вычисляемое свойство (обертка для таблицы) - статистика заданий */
const statInfo = computed(() => {
    const categories = Array.from(new Set<string>(store.task?.jobs.map(job => job.category === "" ? "" : job.category))).sort();
    return categories.map(c => ({
        categoryLabel: c,
        data: [
            {
                label: "Заданий",
                count: store.task?.jobs.reduce((prev,cur) => cur.category === c ? prev+=1 : prev, 0),
                netWeight: store.task?.jobs.reduce((prev,cur) => cur.category === c ? prev+=cur.task_net_weight : prev, 0)
            },
            {
                label: "Выполнено",
                count: store.task?.jobs ? sumJobsStatus(store.task.jobs, true) : 0,
                netWeight: store.task?.jobs.reduce((prev,cur) => cur.done && cur.category === c ? prev+=cur.task_net_weight : prev, 0)
            },
            {
                label: "Осталось",
                count: store.task?.jobs ? sumJobsStatus(store.task.jobs, false) : 0,
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

/** Подсветка строк по статусе */
const rowClassName = ({ row }: { row: frontend.IJob }) => {
    if (statInfo.value.length < 2) return "";
    if (row.category === queryParams.categoryTask && !row.done) {
        return "category-row";
    }
    if (row.done) {
        return "row-done";
    }
    return "";
};
// const filterHandler = (value: string, row: frontend.IJob) => {
//     const isDone = value === "true" ? true : false;
//     return row.done === isDone;
// };
</script>
<style>
.sticky-row {
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: var(--el-fill-color-blank);
}
.category-row {
    background-color: #66b1ff5e !important;
}
.row-done {
    background-color: #66ff7291 !important;
}
</style>
