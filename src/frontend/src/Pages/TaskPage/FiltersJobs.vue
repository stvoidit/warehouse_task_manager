<template>
    <el-row :gutter="10">
        <el-col v-bind="colAttr">
            <div><small>Фильтр по статусу выполнения</small></div>
            <el-select
                placeholder="Статус"
                :model-value="selectedStatuses"
                @change="(value: number) => emit('update:selectedStatuses', value)">
                <el-option
                    v-for="item in statusesOptions"
                    :key="item.label"
                    :label="item.label"
                    :value="item.value" />
            </el-select>
        </el-col>
        <el-col
            v-if="categoriesOptions.length>1"
            class="mb"
            v-bind="colAttr">
            <div><small>Фильтр по статусу выполнения</small></div>
            <el-select
                multiple
                clearable
                :model-value="selectedCategorits"
                placeholder="Категории"
                @change="(value: string[]) => emit('update:selectedCategorits', value)">
                <el-option
                    v-for="item in categoriesOptions"
                    :key="item"
                    :label="item"
                    :value="item" />
            </el-select>
        </el-col>
        <el-col :span="24">
            <span>автообновление: </span>
            <el-switch
                :model-value="autofetch"
                size="small"
                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                @change="(value) => emit('update:autofetch', Boolean(value))" />
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { PropType } from "vue";
defineProps({
    selectedStatuses: {
        type: Number,
        required: true
    },
    selectedCategorits: {
        type: Array as PropType<string[]>,
        required: true
    },
    categoriesOptions: {
        type: Array as PropType<string[]>,
        required: true
    },
    autofetch: {
        type: Boolean,
        required: true
    }
});
const emit = defineEmits<{
    "update:selectedStatuses": [ value: number ],
    "update:selectedCategorits": [value: string[]],
    "update:autofetch": [ value: boolean ]
}>();
const statusesOptions = [
    {
        label: "Все",
        value: 0
    },
    {
        label: "Выполнено",
        value: 1
    },
    {
        label: "Не выполнено",
        value: 2
    }
];
const colAttr = {
    xs: 12,
    sm: 12,
    md: 12,
    lg: 6,
    xl: 6
};
</script>
