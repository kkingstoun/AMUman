import { api } from '$stores/Auth';
import type { CustomUser, AuthUser } from './Api';



function RegisterNewUser(username: string, password: string, email: string) {
    let auth_user: AuthUser = {
        id: 1,
        password: "string",
        username: "string",
    };
    let user: CustomUser = { username: username, password: password, email: email, concurrent_jobs: 0, auth: auth_user };
    api.usersCreate(user).then((res) => {
        console.log('User created', res);
    });
}