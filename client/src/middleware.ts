import { NextResponse, NextRequest } from "next/server";
import axios from 'axios';

export async function authMiddleware(req: NextRequest) {
    const token = req.cookies.get("jwtToken");
    if (!token) {
        return NextResponse.redirect("/auth/login");
    }

    try {
        const jwtcheck = axios.post('http://localhost:5000/api/checkforjwt', {"jwtToken": token})
        if((await jwtcheck).status == 200){
            return NextResponse.next();
        }

    } catch (error) {
        console.error("JWT Token validation failed:", error);
        return NextResponse.redirect("/auth/login");
    }
}

export const middleware = async (req: NextRequest) => {
    if (req.nextUrl.pathname === "/dashboard") {
        return authMiddleware(req);
    } else {
        return NextResponse.next();
    }
};

export const config = {
    api: {
        bodyParser: false,
    },
};
