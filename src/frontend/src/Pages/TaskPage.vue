<template>
    <el-container>
        <el-main>
            <el-row>
                Задача: №{{ taskID }}
            </el-row>
            <br>
            <!-- <pre>{{ store.positions }}</pre> -->
            <el-row>
                <el-table
                    :data="store.positions"
                    :border="true"
                    style="width: 100%"
                    @row-click="handleClickRow">
                    <el-table-column
                        v-for="col in columns"
                        :key="col.prop"
                        :prop="col.prop"
                        :label="col.label" />
                    <el-table-column label="Operations">
                        <template #default="scope">
                            <!-- TODO: обработка клика отдельным хэндлером после подтверждения бэком -->
                            <el-checkbox
                                v-model="scope.row.done"
                                size="large" />
                        </template>
                    </el-table-column>
                </el-table>
            </el-row>
        </el-main>
    </el-container>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useApplicationStore } from "@/store";
export default defineComponent({
    props: {
        taskID: { type: Number, required: true }
    },
    setup(props) {
        const store = useApplicationStore();
        onMounted(() => {
            if (isNaN(props.taskID)) location.href = "/";
            store.fetchTaskPositions(props.taskID);
        });
        const handleClickRow = (row: frontend.ITaskPosition) => {
            if (row.done) {
                row.done = !row.done;
            } else {
                row.done = true;
            }
        };
        const columns = [
            {
                prop: "material",
                label: "material"
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
                label: "tare_id"
            },
            {
                prop: "tare_mark",
                label: "tare_mark"
            },
            {
                prop: "tare_type",
                label: "tare_type"
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
                label: "rest_tare_amount"
            },
            {
                prop: "rest_gross_weight",
                label: "rest_gross_weight"
            },
            {
                prop: "task_tare_amount",
                label: "task_tare_amount"
            },
            {
                prop: "task_net_weight",
                label: "task_net_weight"
            }
        ];
        return {
            store,
            columns,
            handleClickRow
        };
    }
});
</script>
