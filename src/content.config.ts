import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "zod";
import { SITE } from "@/config";

export const BLOG_PATH = "src/data/blog";

const blog = defineCollection({
  loader: glob({ pattern: "**/[^_]*.md", base: `./${BLOG_PATH}` }),
  schema: ({ image }) =>
    z.object({
      author: z.string().default(SITE.author),
      pubDatetime: z.date(),
      modDatetime: z.date().optional().nullable(),
      title: z.string(),
      featured: z.boolean().optional(),
      draft: z.boolean().optional(),
      wip: z.boolean().default(false),
      tags: z.array(z.string()).default(["others"]),
      ogImage: image().or(z.string()).optional(),
      description: z.string(),
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
    }),
});

const projects = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/data/projects" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    stack: z.array(z.string()).default([]),
    repo: z.url().optional(),
    live: z.url().optional(),
    status: z.enum(["active", "archived", "wip"]).default("active"),
  }),
});

export const collections = { blog, projects };
