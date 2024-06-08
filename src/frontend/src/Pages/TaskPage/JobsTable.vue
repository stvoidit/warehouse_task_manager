<template>
    <el-row class="mb">
        <el-col>
            <el-dialog
                v-model="dialogVisible"
                :show-close="false"
                title="Введите остаток веса брутто и/или укажите дополнительный вид обработки материала"
                :align-center="true"
                :width="isLandscape ? '33%': '100%'"
                @close="resetDialoagForm">
                <el-form
                    v-if="dialogJob"
                    label-position="top">
                    <el-form-item label="Остаток (брутто)">
                        <el-input-number
                            v-model="takenWeight"
                            size="large"
                            :precision="2"
                            :min="dialogJob.tara_weight"
                            :max="dialogJob.rest_gross_weight" />
                    </el-form-item>
                    <el-form-item label="Вид дополнительной обработки">
                        <el-select
                            v-model="dialogJob.add_processing_id"
                            size="large"
                            :disabled="blockActionRow(dialogJob)"
                            fit-input-width>
                            <el-option
                                :value="0"
                                label=" " />
                            <el-option
                                v-for="pt in processingTypes"
                                :key="pt.id"
                                :label="pt.process_name"
                                :value="pt.id" />
                        </el-select>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <span class="dialog-footer">
                        <el-button @click="dialogVisible = false">
                            Закрыть
                        </el-button>
                        <el-button
                            v-if="dialogJob"
                            type="success"
                            :disabled="takenWeight === null"
                            @click="handleDialogWeight(dialogJob, takenWeight)">
                            Подтвердить
                        </el-button>
                    </span>
                </template>
            </el-dialog>
            <DialogRestGrossWeight
                v-model:dialogVisible="dialogVisibleRGW"
                v-model:job="dialogJob"
                :is-landscape="isLandscape"
                @change-r-g-w="(value) => emit('changeRGW', value)" />
            <el-table
                :data="jobsList"
                :border="true"
                :row-key="rowKey"
                :cell-style="cellStyle"
                :row-class-name="rowClass"
                @row-click="handleClickRow">
                <el-table-column
                    :width="80"
                    prop="done"
                    column-key="done"
                    label="">
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
                    :min-width="col.width"
                    :formatter="col.formatter" />
                <el-table-column
                    :width="150"
                    prop="add_processing_id"
                    column-key="add_processing_id"
                    label="Доп. обработка">
                    <template #default="{ row }: { row: frontend.IJob }">
                        {{ processingTypes.find(pt => pt.id === row.add_processing_id)?.process_name }}
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { PropType, ref } from "vue";
import { ElMessageBox } from "element-plus";
import DialogRestGrossWeight from "./DialogRestGrossWeight.vue";
defineProps({
    jobsList: {
        type: Array as PropType<frontend.IJob[]>,
        required: true
    },
    processingTypes: {
        type: Array as PropType<frontend.IProcessingType[]>,
        default: () => [] as frontend.IProcessingType[]
    },
    isLandscape: {
        type: Boolean,
        default: true
    }
});
const emit = defineEmits<{
    /** эмит оригинальной работы + вес который списываем фактически */
    changeStatus: [value: frontend.IJob, weight: number],
    processingChange: [value: boolean],
    changeRGW: [value:frontend.IJob]
}>();
const rowKey = (row: frontend.IJob) => `${row.material_id}-${row.tare_id}`;
const cellStyle = ({ column }: { column: any }) => {
    if ([
        "net_weight_fact",
        "add_processing_id",
        "rest_gross_weight"
    ].includes(column.columnKey)) {
        return { cursor: "alias" };
    }
    if (column.columnKey === "tare_id") {
        return {
            fontSize: "18px",
            fontWeight: "bold"
        };
    }
    return {};
};
const rowClass = ( {row } : { row: frontend.IJob }) => blockActionRow(row) ? "row-disabled" : "";
const blockActionRow = (job: frontend.IJob) => job.done === true && job.add_processing_id > 0;
const dialogVisible = ref(false);
const dialogJob = ref<frontend.IJob | null>(null);
const takenWeight = ref(0);
const resetDialoagForm = () => {
    /** копия frontend.IJob */
    dialogJob.value = null;
    /** ВЕС БРУТТО!!! ФАКТ (НЕТТО) СЧИТАЕМ В ОТПРАВЕ ЗАПРОСА */
    takenWeight.value = 0;
};

const dialogVisibleRGW = ref(false);

/** Обработчик клика на строку - запрос на обновление статуса задания */
const handleClickRow = async (job: frontend.IJob, column: any) => {
    const targetCols = [
        "net_weight_fact",
        "add_processing_id"
    ];
    if (column.columnKey === "rest_gross_weight" && job.task_net_weight === 0) {
        dialogJob.value = { ...job };
        dialogVisibleRGW.value = true;
        return;
    }
    if (!targetCols.includes(column.columnKey) && job.done && job.add_processing_id > 0) return;
    if (targetCols.includes(column.columnKey)) {
        dialogVisible.value = true;
        dialogJob.value = { ...job };
        if (dialogJob.value.done) dialogJob.value.done = false;
        takenWeight.value = dialogJob.value.net_weight_fact > 0 ? dialogJob.value.task_net_weight + dialogJob.value.tara_weight - dialogJob.value.net_weight_fact : dialogJob.value.tara_weight;
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

/**
 * При вводе в диалоге - вводится ОСТАТОК В ТАРЕ,
 * поэтому необходимо высчитать взятый ГРОСС вес.
 * Особенность костылинга
 */
const handleDialogWeight = (job: frontend.IJob, weight: number) => {
    emit("changeStatus", job, (job.rest_gross_weight - weight) + job.tara_weight);
    dialogVisible.value = false;
};
const numberFormatter = (row: any, col: any, cellValue: number) => cellValue.toLocaleString();
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
        prop: "category",
        label: "Категория",
        width: 150,
        sortable: true
    },
    {
        prop: "tare_type",
        label: "Тара",
        width: 100,
        sortable: false
    },
    {
        prop: "rest_gross_weight",
        label: "Брутто",
        // width: 100,
        sortable: false,
        formatter: numberFormatter
    },
    {
        prop: "task_net_weight",
        label: "Задание",
        // width: 100,
        sortable: false,
        formatter: numberFormatter
    },
    {
        prop: "net_weight_fact",
        label: "Выполнено",
        // width: 110,
        sortable: false,
        formatter: numberFormatter
    }
];
</script>
