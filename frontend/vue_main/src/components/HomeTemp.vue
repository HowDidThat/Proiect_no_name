<template>
    <div>
      <section class="vh-100 gradient-custom">
        <div class=" vh-100 page_404">
          <p>
            #404 Page not found.
          </p>
          <p>
            You silly goose.
          </p>
        </div>
        </section>
    </div>
</template>

<script>
export default {
    name: "HomeTemp"
}
</script>

<style scoped>
.gradient-custom {
  background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}
  
.page_404{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: xx-large
}
</style>