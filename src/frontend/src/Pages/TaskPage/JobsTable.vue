<template>
    <el-row class="mb">
        <el-col>
            <el-table
                :data="jobsList"
                :border="true"
                :row-key="rowKey"
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

defineProps({
    jobsList: {
        type: Array as PropType<frontend.IJob[]>,
        required: true
    }
});
const emit = defineEmits<{
    changeStatus: [ value: frontend.IJob ]
}>();
const rowKey = (row:frontend.IJob) => `${row.material_id}-${row.tare_id}`;

/** Обработчик клика на строку - запрос на обновление статуса задания */
const handleClickRow = (row: frontend.IJob, column: any) => {
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
    },
    {
        prop: "net_weight_fact",
        label: "Нетто (факт)",
        width: 150,
        sortable: false
    }
];
</script>
