<script setup lang="ts">
import FileUploadArea from '@/components/ui/file-upload-area.vue'
import { ref } from 'vue'

const file = ref(null)
</script>

<template>
    <form
        class="bg-neutral-100 rounded-lg max-w-[1080px] px-8 py-7 min-h-72"
        @submit.prevent=""
    >
        <FileUploadArea v-model="file" />
    </form>
</template>
