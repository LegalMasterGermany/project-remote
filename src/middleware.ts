import { NextResponse, type NextRequest } from "next/server";

export function middleware(req: NextRequest){

   const jwttoken = req.cookies.get("jwtToken")
   if(!jwttoken){
    return NextResponse.redirect(new URL("/auth/login", req.url))
   }
}

export const config = {
    matcher: "/dashboard"
}