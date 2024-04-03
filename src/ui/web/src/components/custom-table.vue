<script setup lang="ts">
defineProps<{
    items: Record<string, string | number>[]
}>()
</script>

<template>
    <table class="table bg-white ring-1 ring-neutral-200 rounded-lg overflow-hidden">
        <thead>
            <tr>
                <th
                    v-for="heading in Object.keys(items[0] || {})"
                    :key="heading"
                    class="font-medium text-start bg-neutral-50 border-r border-b border-neutral-200 text-[15px] px-7 py-3.5 last:border-r-0"
                >
                    {{ heading }}
                </th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="row in items" class="transition-colors duration-200 hover:bg-red-100/30">
                <td v-for="cell in row" class="px-7 py-3.5">
                    {{ cell }}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>

</style>
