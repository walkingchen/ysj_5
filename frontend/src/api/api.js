import axios from 'axios'
import { base } from "../config/index"

export const requestLogin = () => {
    return axios.get(`${base}`).then(res => res.data);
};