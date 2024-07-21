<script setup lang="ts">
import FilledButton from '@/components/ui/filled-button.vue'
import ExportIcon from '@/components/ui/icons/export-icon.vue'
import { SpokenTextStats } from '@/types/spoken-text-stats'
import csv from 'csv'

const props = defineProps<{
    statsToExport: SpokenTextStats
}>()

function exportStats() {
    csv.generate({
        columns: []
    })
}
</script>

<template>
    <FilledButton>
        <ExportIcon class="w-5" />
        export
    </FilledButton>
</template>
