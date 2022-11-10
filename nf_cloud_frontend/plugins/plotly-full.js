import Plotly from "plotly.js-dist";
import vue from "vue";

vue.use(Plotly);
export default (_, inject) => {
    inject('plotly', Plotly)
}