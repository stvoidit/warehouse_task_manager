<template>
    <el-row class="mb">
        <el-col>
            <el-table
                :data="jobsList"
                :border="true"
                :row-key="rowKey"
                :row-class-name="rowClassName"
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
                                :disabled="disabledRow(row)"
                                size="large"
                                @change.capture="emit('changeStatus', row)" />
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

interface IRemainingWeight {[key: string]: number}
const props = defineProps({
    jobsList: {
        type: Array as PropType<frontend.IJob[]>,
        required: true
    },
    remainingWeight: {
        type: Object as PropType<IRemainingWeight>,
        default: ():IRemainingWeight => ({})
    }
});
const emit = defineEmits<{
    changeStatus: [ value: frontend.IJob ]
}>();
const rowKey = (row:frontend.IJob) => `${row.material_id}-${row.tare_id}`;

/** расчет по весу категории нужно ли блокировать ввод */
const disabledRow = (row: frontend.IJob) => {
    const categoryRemainingWeight = props.remainingWeight[row.category];
    if (!categoryRemainingWeight) return false;
    if (row.task_net_weight > categoryRemainingWeight && row.done === false) return true;
    return false;
};
/** расчет CSS класса для строки */
const rowClassName = ({ row }: { row: frontend.IJob }) => {
    if (disabledRow(row) === true) return "row-disabled";
    return "";
};
/** Обработчик клика на строку - запрос на обновление статуса задания */
const handleClickRow = (row: frontend.IJob, column: any) => {
    if (disabledRow(row) === true && row.done === false) return;
    if (column.no === 0) return;
    emit("changeStatus", row);
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
    }
];
</script>
