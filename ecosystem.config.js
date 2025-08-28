module.exports = {
  apps: [{
    name: "SARU",
    // PERUBAHAN 1: Cukup panggil 'python'
    script: "python",
    
    // PERUBAHAN 2: Argumennya tetap sama
    args: "-m waitress --port=11005 app:app", 
    
    // PERUBAHAN 3: Tidak perlu interpreter
    interpreter: "none",
    
    watch: true,
    env: {
      "NODE_ENV": "development",
    },
    env_production: {
      "NODE_ENV": "production",
    }
  }]
};