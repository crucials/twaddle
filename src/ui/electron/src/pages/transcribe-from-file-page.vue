<script setup lang="ts">
import TranscriptionOptionsInputs from '@/components/transcription-options-inputs.vue'
import FileUploadArea from '@/components/ui/file-upload-area.vue'
import FilledButton from '@/components/ui/filled-button.vue'
import SpokenTextStatsView from '@/components/spoken-text-stats-view.vue'
import Spinner from '@/components/ui/spinner.vue'
import { TranscriptionOptions } from '@/types/transcription-options'
import { SpokenTextStats } from '@/types/spoken-text-stats'
import { useApi } from '@/composables/api'
import { reactive, ref } from 'vue'

const { fetchWithErrorNotification } = useApi()

const formData = reactive<TranscriptionOptions & {
    file: File | null
}>({
    file: null,
    language: null,
    wordListName: null,
})

const result = ref<SpokenTextStats>()
const loading = ref(false)

async function startTranscribing() {
    if(!formData.file) {
        return
    }

    const requestFormData = new FormData()
    requestFormData.set('audio_file', formData.file)

    if(formData.language) {
        requestFormData.set('language', formData.language)
    }
    if(formData.wordListName) {
        requestFormData.set('word_list_name', formData.wordListName)
    }

    loading.value = true
    
    const response = await fetchWithErrorNotification('/audio-file-word-counter', {
        method: 'POST',
        body: requestFormData,
        headers: new Headers()
    })

    loading.value = false

    if(response.data) {
        result.value = {
            fullText: response.data.full_text,
            wordsStats: response.data.words_stats
        }
    }
}
</script>

<template>
    <Transition
        enter-active-class="transition-opacity duration-300"
        leave-active-class="transition-opacity duration-300"
        enter-from-class="absolute opacity-0"
        leave-to-class="absolute opacity-0"
    >
        <form
            v-if="!result && !loading"
            class="bg-neutral-100 rounded-lg max-w-[1080px] px-8 py-7 min-h-72
                flex gap-x-5 gap-y-7 items-start justify-items-start flex-wrap"
            @submit.prevent="startTranscribing"
        >
            <FileUploadArea v-model="formData.file" accept=".mp3, .wav" class="min-w-2">
                <div class="mb-2">
                    speech language
                </div>
            </FileUploadArea>

            <Suspense>
                <TranscriptionOptionsInputs
                    v-model:language="formData.language"
                    v-model:word-list-name="formData.wordListName"
                />
            </Suspense>

            <div class="w-full">
                <FilledButton>
                    transcribe
                </FilledButton>
            </div>
        </form>
        
        <Spinner v-else-if="!result && loading" class="mb-5" />

        <SpokenTextStatsView
            v-else-if="result"
            :stats="result"
        >
            <template #no-words-fallback>
                no words were found, they are either not in the selected word list
                or can't be detected
            </template>
        </SpokenTextStatsView>
    </Transition>
</template>
