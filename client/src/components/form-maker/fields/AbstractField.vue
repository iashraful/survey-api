<template>
  <div class="text-input">
    <b-field
      :label="field.title"
      :message="(displayErrorMgs && errorText !== '') ? errorText : ''"
      :type="(displayErrorMgs && errorText !== '') ? 'is-danger' : ''">
      <b-input v-model="value" type="text"></b-input>
    </b-field>
  </div>
</template>

<script>
export default {
  name: 'AbstractField',
  props: ['field', 'submitted'],
  data () {
    return {
      value: '',
      errorText: '',
      displayErrorMgs: false
    }
  },
  methods: {
    isValid (raiseExp = true) {
      const _data = {
        field: this.field,
        [this.field.name]: this.value,
        status: false
      }
      if (!raiseExp) {
        _data.status = false
      } else {
        if (this.field.required && this.value === '') {
          this.errorText = 'This field is required.'
          _data.status = false
        } else {
          this.errorText = ''
          _data.status = true
        }
      }
      return _data
    },
    validate () {
      const _data = this.isValid()
      this.$emit('validate', _data)
    }
  },
  mounted () {
    this.validate()
  },
  watch: {
    value (newVal) {
      this.displayErrorMgs = true
      this.validate()
    },
    submitted (newVal) {
      // This will call only once it'll trigger submit button
      if (newVal) {
        this.displayErrorMgs = true
        this.validate()
      }
    }
  }
}
</script>

<style scoped>
.text-input input {
  width: 100%
}

.text-input .error {
  color: red;
}
</style>
