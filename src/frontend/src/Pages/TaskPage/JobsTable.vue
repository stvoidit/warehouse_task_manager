<template>
    <el-row class="mb">
        <el-col>
            <el-table
                :data="jobsList"
                :border="true"
                :row-key="rowKey"
                :cell-style="cellStyle"
                :row-class-name="rowClass"
                @row-click="handleClickRow">
                <el-table-column
                    :width="100"
                    prop="done"
                    column-key="done"
                    label="Выполнено">
                    <template #default="{ row }: { row: frontend.IJob }">
                        <div
                            style="text-align: center;"
                            @click.prevent>
                            <el-checkbox
                                :model-value="row.done"
                                :disabled="blockActionRow(row)" />
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
                <el-table-column
                    :width="180"
                    prop="add_processing_id"
                    column-key="add_processing_id"
                    label="Тип процесса">
                    <template #default="{ row }: { row: frontend.IJob }">
                        <el-select
                            v-model="row.add_processing_id"
                            :disabled="blockActionRow(row)"
                            fit-input-width
                            @visible-change="emit('processingChange', true)">
                            <el-option
                                :value="0"
                                label=" " />
                            <el-option
                                v-for="pt in processingTypes"
                                :key="pt.id"
                                :label="pt.process_name"
                                :value="pt.id" />
                        </el-select>
                    </template>
                </el-table-column>
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
    },
    processingTypes: {
        type: Array as PropType<frontend.IProcessingType[]>,
        default: () => [] as frontend.IProcessingType[]
    }
});
const emit = defineEmits<{
    /** эмит оригинальной работы + вес который списываем фактически */
    changeStatus: [value: frontend.IJob, weight: number],
    processingChange: [value: boolean]
}>();
const rowKey = (row: frontend.IJob) => `${row.material_id}-${row.tare_id}`;
const cellStyle = ({ column }: { column: any }) => column.columnKey === "net_weight_fact" ? { cursor: "alias" } : {};
const rowClass = ( {row } : { row: frontend.IJob }) => blockActionRow(row) ? "row-disabled" : "";
const blockActionRow = (job: frontend.IJob) => job.done === true && job.add_processing_id > 0;

/** Обработчик клика на строку - запрос на обновление статуса задания */
const handleClickRow = async (job: frontend.IJob, column: any) => {
    if (blockActionRow(job)) return;
    if (column.columnKey === "add_processing_id") return;
    if (column.columnKey === "net_weight_fact" && job.done === false) {
        try {
            const { value } = await ElMessageBox.prompt(
                "Введите остаток веса брутто",
                {
                    confirmButtonText: "Подтверждение",
                    cancelButtonText: "Отмена",
                    type: "info",
                    inputType: "number",
                    inputValue: job.rest_gross_weight.toFixed(2),
                    inputPattern: /^\d+\.?\d{0,2}?$/,
                    inputValidator: (value) => {
                        if (parseFloat(value) > job.rest_gross_weight) {
                            return "Превышение допустимого ввода веса брутто";
                        }
                        if (parseFloat(value) < job.tara_weight) {
                            return "Вес брутто не может быть меньше веса тары";
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
    } else if (column.columnKey === "net_weight_fact" && job.done === true && job.task_net_weight !== job.net_weight_fact) {
        try {
            const { value } = await ElMessageBox.prompt(
                "Введите остаток веса брутто",
                {
                    confirmButtonText: "Подтверждение",
                    cancelButtonText: "Отмена",
                    type: "info",
                    inputType: "number",
                    inputValue: (job.net_weight_fact+job.tara_weight).toFixed(2),
                    inputPattern: /^\d+\.?\d{0,2}?$/,
                    inputValidator: (value) => {
                        if (parseFloat(value) > job.rest_gross_weight) {
                            return "Превышение допустимого ввода веса брутто";
                        }
                        if (parseFloat(value) < job.tara_weight) {
                            return "Вес брутто не может быть меньше веса тары";
                        }
                        return true;
                    }
                }
            );
            const fateJob = { ...job };
            fateJob.done = false;
            emit("changeStatus", fateJob, parseFloat(value));
        } catch (error) {
            // eslint-disable-next-line
                console.warn(error);
            return;
        }
    } else {
        if (job.done === true && job.task_net_weight !== job.net_weight_fact) {
            try {
                await ElMessageBox.confirm(
                    "Предупреждение",
                    {
                        message: "Взятый вес был введен вручную. Хотите изменить статус выполнения на \"не выполнено\"?",
                        confirmButtonText: "Да",
                        cancelButtonText: "Нет",
                        type: "warning"
                    }
                );
            } catch (error) {
                // eslint-disable-next-line
                console.warn(error);
                return;
            }
        }
        emit("changeStatus", job, job.rest_gross_weight);
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
        label: "Нетто (взято)",
        width: 150,
        sortable: false
    }
];
</script>
