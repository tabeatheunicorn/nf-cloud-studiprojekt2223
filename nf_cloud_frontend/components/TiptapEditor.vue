<template>
    <editor-content :editor="editor" />
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-2'
import StarterKit from '@tiptap/starter-kit'

export default {
    components: {
        EditorContent,
    },

    data() {
        return {
            editor: null,
        }
    },

    mounted() {
        this.editor = new Editor({
            content: '<h1>Example Workflow Editor</h1>',
            extensions: [
                StarterKit,
            ],
        })
    },

    beforeDestroy() {
        this.editor.destroy()
    },
}
</script>
