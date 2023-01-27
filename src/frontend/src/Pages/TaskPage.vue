<template>
    <el-row v-if="store.isAuth">
        <el-col v-loading="store.loading">
            <!-- <pre>{{ store.task }}</pre> -->
            <el-row class="mb">
                {{ store.task?.doc_number }}
            </el-row>
            <el-row
                class="mb"
                :gutter="20">
                <el-col
                    :xs="12"
                    :sm="12"
                    :md="12"
                    :lg="8"
                    :xl="6">
                    <el-table
                        :data="metaInfo"
                        :border="true"
                        :show-header="false"
                        size="small">
                        <el-table-column
                            prop="label"
                            :width="150" />
                        <el-table-column
                            prop="value" />
                    </el-table>
                </el-col>
                <el-col
                    :xs="12"
                    :sm="12"
                    :md="12"
                    :lg="8"
                    :xl="6">
                    <el-table
                        :data="statInfo"
                        :border="true"
                        :show-header="false"
                        size="small">
                        <el-table-column
                            prop="label"
                            :width="150" />
                        <el-table-column
                            prop="value" />
                    </el-table>
                </el-col>
            </el-row>
            <el-row>
                <el-table
                    :data="store.task?.jobs"
                    :border="true"
                    size="small"
                    style="width: 100%"
                    @row-click="handleClickRow">
                    <el-table-column
                        v-for="col in columns"
                        :key="col.prop"
                        :prop="col.prop"
                        :label="col.label" />
                    <el-table-column
                        width="100"
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
                </el-table>
            </el-row>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter } from "vue-router";
import { useApplicationStore } from "@/store";
import { ElMessage } from "element-plus";
export default defineComponent({
    props: {
        /** ID склада */
        stockID: { type: Number, required: true },
        /** ID задачи */
        taskID: { type: Number, required: true },
        /** ID материала */
        materialID: { type: Number, required: true }
    },
    setup(props) {
        const router = useRouter();
        const store = useApplicationStore();
        /**
         * 1) Получение данных задачи
         * 2) Запуск автообновления
         */
        onMounted(() => {
            if (isNaN(props.taskID)) router.push("/");
            store.fetchTask(props.stockID, props.taskID, props.materialID);
            store.doAutofetch(props.stockID, props.taskID, props.materialID);
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
                await store.fetchTask(props.stockID, props.taskID, props.materialID);
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
            if (column.no === 8) return;
            updateJobStatus(row.tare_id, !row.done, row.tare_mark);
        };
        /** Функция для подсчета кол-ва заданий по статусу */
        const sumJobsStatus = (jobs: Array<frontend.IJob>, status: boolean) => jobs.reduce((prev, job) => prev = job.done === status ? prev + 1 : prev, 0);
        /** Вычисляемое свойство (обертка для таблицы) - метаданные задачи */
        const metaInfo = computed(() => ([
            {
                label: "Материал",
                value: store.task?.material
            },
            {
                label: "Техпроцесс",
                value: store.task?.technical_process
            },
            {
                label: "Операция",
                value: store.task?.operation
            }
        ]));
        /** Вычисляемое свойство (обертка для таблицы) - статистика заданий */
        const statInfo = computed(() => ([
            {
                label: "Заданий",
                value: store.task?.jobs ? store.task.jobs.length : 0
            },
            {
                label: "Выполнено",
                value: store.task?.jobs ? sumJobsStatus(store.task.jobs, true) : 0
            },
            {
                label: "Осталось",
                value: store.task?.jobs ? sumJobsStatus(store.task.jobs, false) : 0
            }
        ]));
        /** Список столбцов таблицы */
        const columns = [
            {
                prop: "material",
                label: "Материал"
            },
            {
                prop: "tare_id",
                label: "Номер тары"
            },
            {
                prop: "tare_mark",
                label: "Маркировка тары"
            },
            {
                prop: "tare_type",
                label: "Тара"
            },
            {
                prop: "rest_tare_amount",
                label: "Кол-во"
            },
            {
                prop: "rest_gross_weight",
                label: "Вес брутто"
            },
            {
                prop: "task_tare_amount",
                label: "Задание кол-во"
            },
            {
                prop: "task_net_weight",
                label: "Задание вес нетто"
            }
        ];
        return {
            store,
            columns,
            handleClickRow,
            updateJobStatus,
            metaInfo,
            statInfo
        };
    }
});
</script>
