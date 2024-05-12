<script setup lang="ts">
import TranscriptionOptionsInputs from '@/components/transcription-options-inputs.vue'
import FileUploadArea from '@/components/ui/file-upload-area.vue'
import FilledButton from '@/components/ui/filled-button.vue'
import { reactive, ref } from 'vue'
import { TranscriptionOptions } from '@/types/transcription-options'

const formData = reactive<TranscriptionOptions & {
    file: File | null
}>({
    file: null,
    language: null,
    wordListName: null,
})

function startTranscribing() {
    console.log(formData)
}
</script>

<template>
    <form
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
</template>
