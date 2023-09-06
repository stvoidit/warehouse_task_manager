<template>
    <el-row :gutter="20">
        <el-col
            v-for="cat in statInfo"
            :key="cat.categoryLabel"
            class="mb"
            v-bind="colAttr">
            <div :style="{minHeight: '1.3rem', padding: '0.25rem'}">
                <b style="margin-right: 0.3rem;">{{ cat.categoryLabel }}</b>
                <el-popover
                    v-if="catmat[cat.categoryLabel]"
                    :width="200"
                    trigger="click">
                    <template #reference>
                        <el-button
                            size="small"
                            type="primary"
                            icon="tickets"
                            circle />
                    </template>
                    <b>материалы:</b>
                    <ul>
                        <li
                            v-for="mat in catmat[cat.categoryLabel].split(',')"
                            :key="mat">
                            {{ mat }}
                        </li>
                    </ul>
                </el-popover>
            </div>
            <el-table
                :data="cat.data"
                :border="true"
                :show-header="false"
                table-layout="auto">
                <el-table-column
                    prop="label"
                    :width="150" />
                <el-table-column
                    prop="count"

                    :formatter="numberFormatter" />
                <el-table-column

                    :formatter="numberFormatter"
                    prop="netWeight" />
            </el-table>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { PropType } from "vue";
interface IStatInfo {
    categoryLabel: string;
    data: {
        label: string;
        count: number | undefined;
        netWeight: number | undefined;
    }[];
}[];
defineProps({
    statInfo: {
        type: Array as PropType<IStatInfo[]>,
        required: true
    },
    catmat: {
        type: Object as PropType<frontend.ICatMat>,
        default: () => ({})
    }
});
const numberFormatter = (row: any, col: any, cellValue: number) => cellValue.toLocaleString();
const colAttr = {
    xs:24,
    sm:12,
    md:12,
    lg:8,
    xl:6
};
</script>
