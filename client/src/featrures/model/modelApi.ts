import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { Model } from "./type";

export const apiSlice = createApi({
  reducerPath: "model",
  baseQuery: fetchBaseQuery({ baseUrl: `http://localhost:3500` }),
  endpoints: (builder) => ({
    getModels: builder.query<Model[], void>({
      query: () => `/get-scripts`,
    }),
  }),
});

export const { useGetModelsQuery } = apiSlice;
