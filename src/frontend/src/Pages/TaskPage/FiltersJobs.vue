<template>
    <el-row
        :gutter="10"
        style="margin-top: 0.75rem;">
        <el-col v-bind="colAttr">
            <div><small>Фильтр по статусу выполнения</small></div>
            <el-select
                placeholder="Статус"
                size="large"
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
            <div><small>Фильтр по категории</small></div>
            <el-select
                multiple
                clearable
                size="large"
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
    }
});
const emit = defineEmits<{
    "update:selectedStatuses": [ value: number ],
    "update:selectedCategorits": [value: string[]]
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
