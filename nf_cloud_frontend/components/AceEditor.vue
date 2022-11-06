<template>
    <v-ace-editor
        v-model:value="content"
        @init="editorInit"
        lang="html"
        theme="chrome"
        style="height: 300px" />
</template>

<script>
import { VAceEditor } from 'vue3-ace-editor';

export default {
    components: {
        VAceEditor
    }
}
</script>
