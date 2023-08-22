<template>
    <el-row class="mb">
        <el-col>
            <el-table
                :data="jobsList"
                :border="true"
                :row-key="rowKey"
                :cell-style="cellStyle"
                @row-click="handleClickRow">
                <el-table-column
                    :width="100"
                    prop="done"
                    column-key="done"
                    label="Выполнено">
                    <template #default="{ row }: { row: frontend.IJob }">
                        <div style="text-align: center;">
                            <el-checkbox
                                v-model="row.done"
                                size="large"
                                @change.capture="emit('changeStatus', row, row.task_net_weight)" />
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
</template>

<script setup lang="ts">
import { PropType } from "vue";
import { ElMessageBox } from "element-plus";

defineProps({
    jobsList: {
        type: Array as PropType<frontend.IJob[]>,
        required: true
    }
});
const emit = defineEmits<{
    /** эмит оригинальной работы + вес который списываем фактически */
    changeStatus: [ value: frontend.IJob, weight: number ]
}>();
const rowKey = (row: frontend.IJob) => `${row.material_id}-${row.tare_id}`;
const cellStyle = ({ column }: { column:any }) => column.columnKey === "net_weight_fact" ? {cursor:"alias"} : {};

/** Обработчик клика на строку - запрос на обновление статуса задания */
const handleClickRow = async (job: frontend.IJob, column: any) => {
    if (column?.no === 0) return;
    if (column.columnKey === "net_weight_fact" && job.done === false) {
        try {
            const { value } = await ElMessageBox.prompt(
                "Введите вес списания",
                {
                    confirmButtonText: "Подтверждение",
                    cancelButtonText: "Отмена",
                    type: "info",
                    inputType: "number",
                    inputValue: job.task_net_weight.toFixed(2),
                    inputPattern: /^\d+\.?\d{0,2}?$/,
                    inputValidator: (value) => {
                        if (parseFloat(value) > job.task_net_weight) {
                            return "Превышение допустимого ввода веса";
                        }
                        return true;
                    }
                }
            );
            emit("changeStatus", job, parseFloat(value));
        } catch (error) {
            // eslint-disable-next-line
                console.warn(error);
            return;
        }
    } else {
        emit("changeStatus", job, job.task_net_weight);
    }
};

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
    },
    {
        prop: "net_weight_fact",
        label: "Нетто (факт)",
        width: 150,
        sortable: false
    }
];
</script>
