<template>
    <el-row v-if="store.isAuth">
        <el-col>
            <!-- <pre>{{ store.task }}</pre> -->
            <el-row class="mb">
                Задача: №{{ taskID }}
            </el-row>
            <el-row
                class="mb"
                :gutter="20">
                <el-col :span="4">
                    <el-table
                        :data="metaInfo"
                        :border="true"
                        :show-header="false"
                        size="small">
                        <el-table-column prop="label" />
                        <el-table-column prop="value" />
                    </el-table>
                </el-col>
                <el-col :span="4">
                    <el-table
                        :data="statInfo"
                        :border="true"
                        :show-header="false"
                        size="small">
                        <el-table-column prop="label" />
                        <el-table-column prop="value" />
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
                    <el-table-column label="Выполнено">
                        <template #default="scope">
                            <!-- TODO: обработка клика отдельным хэндлером после подтверждения бэком -->
                            <el-checkbox
                                v-model="scope.row.done"
                                size="large" />
                        </template>
                    </el-table-column>
                </el-table>
            </el-row>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed } from "vue";
import { useApplicationStore } from "@/store";
export default defineComponent({
    props: {
        taskID: { type: Number, required: true }
    },
    setup(props) {
        const store = useApplicationStore();
        onMounted(() => {
            if (isNaN(props.taskID)) location.href = "/";
            store.fetchTask(props.taskID);
        });
        const handleClickRow = (row: frontend.ITaskPosition) => {
            if (row.done) {
                row.done = !row.done;
            } else {
                row.done = true;
            }
        };
        const sumJobsStatus = (jobs: Array<frontend.ITaskPosition>, status: boolean) => jobs.reduce((prev, job) => prev = job.done === status ? prev+1 : prev, 0);
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
        const columns = [
            {
                prop: "material",
                label: "Материал"
            },
            {
                prop: "lab_material_mark",
                label: "lab_material_mark"
            },
            {
                prop: "lab_material_group",
                label: "lab_material_group"
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
                prop: "arrival_tare_amount",
                label: "arrival_tare_amount"
            },
            {
                prop: "arrival_gross_weight",
                label: "arrival_gross_weight"
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
            metaInfo,
            statInfo
        };
    }
});
</script>
<style>
.simple-table {
    border-collapse: collapse;
}
.simple-table td {
    border: 1px solid #dcdfe6;
    padding: 0.5rem;
}
</style>
