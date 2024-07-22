<script setup lang="ts">
import FilledButton from '@/components/ui/filled-button.vue'
import ExportIcon from '@/components/ui/icons/export-icon.vue'
import { SpokenTextStats } from '@/types/spoken-text-stats'
import { formatSeconds } from '@/utils/format-seconds';
import xlsx from 'xlsx'

const props = defineProps<{
    statsToExport: SpokenTextStats
    secondsSpeaking: number | null
}>()

function exportStats() {
    const basicInfoWorksheet = xlsx.utils.json_to_sheet([{
        fullText: props.statsToExport.fullText,
        timeSpeaking: props.secondsSpeaking !== null ?
            formatSeconds(props.secondsSpeaking) : '-'
    }])
    xlsx.utils.sheet_add_aoa(basicInfoWorksheet, [['full text', 'speaking time (HH:MM:SS)']])

    const wordsCountWorksheet = xlsx.utils.json_to_sheet(
        props.statsToExport.wordsStats.map(statsRecord => ({
            word: statsRecord.word,
            count: statsRecord.count,
        }))
    );

    const workbook = xlsx.utils.book_new()
    xlsx.utils.book_append_sheet(workbook, basicInfoWorksheet, 'basic info')
    xlsx.utils.book_append_sheet(workbook, wordsCountWorksheet, 'words count')

    xlsx.writeFile(workbook, 'speech-statistics.xlsx')
}
</script>

<template>
    <FilledButton @click="exportStats">
        <ExportIcon class="w-5" />
        export
    </FilledButton>
</template>
