--
-- PostgreSQL database dump
--

-- Dumped from database version 11.3 (Debian 11.3-1.pgdg90+1)
-- Dumped by pg_dump version 11.3 (Debian 11.3-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO mgallery;

--
-- Name: gallery; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.gallery (
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    path character varying,
    name character varying
);


ALTER TABLE public.gallery OWNER TO mgallery;

--
-- Name: gallery_id_seq; Type: SEQUENCE; Schema: public; Owner: mgallery
--

CREATE SEQUENCE public.gallery_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gallery_id_seq OWNER TO mgallery;

--
-- Name: gallery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mgallery
--

ALTER SEQUENCE public.gallery_id_seq OWNED BY public.gallery.id;


--
-- Name: image; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.image (
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    path character varying,
    name character varying,
    phash character varying,
    size integer,
    width integer,
    height integer,
    gallery_id integer
);


ALTER TABLE public.image OWNER TO mgallery;

--
-- Name: image_id_seq; Type: SEQUENCE; Schema: public; Owner: mgallery
--

CREATE SEQUENCE public.image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_id_seq OWNER TO mgallery;

--
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mgallery
--

ALTER SEQUENCE public.image_id_seq OWNED BY public.image.id;


--
-- Name: image_to_image; Type: TABLE; Schema: public; Owner: mgallery
--

CREATE TABLE public.image_to_image (
    left_id integer NOT NULL,
    right_id integer NOT NULL
);


ALTER TABLE public.image_to_image OWNER TO mgallery;

--
-- Name: gallery id; Type: DEFAULT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.gallery ALTER COLUMN id SET DEFAULT nextval('public.gallery_id_seq'::regclass);


--
-- Name: image id; Type: DEFAULT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image ALTER COLUMN id SET DEFAULT nextval('public.image_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: mgallery
--

COPY public.alembic_version (version_num) FROM stdin;
7cc447b540fd
\.


--
-- Data for Name: gallery; Type: TABLE DATA; Schema: public; Owner: mgallery
--

COPY public.gallery (id, created_at, path, name) FROM stdin;
\.


--
-- Data for Name: image; Type: TABLE DATA; Schema: public; Owner: mgallery
--

COPY public.image (id, created_at, path, name, phash, size, width, height, gallery_id) FROM stdin;
\.


--
-- Data for Name: image_to_image; Type: TABLE DATA; Schema: public; Owner: mgallery
--

COPY public.image_to_image (left_id, right_id) FROM stdin;
\.


--
-- Name: gallery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mgallery
--

SELECT pg_catalog.setval('public.gallery_id_seq', 1, false);


--
-- Name: image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mgallery
--

SELECT pg_catalog.setval('public.image_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: gallery gallery_pkey; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.gallery
    ADD CONSTRAINT gallery_pkey PRIMARY KEY (id);


--
-- Name: image image_pkey; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_pkey PRIMARY KEY (id);


--
-- Name: image_to_image image_to_image_pkey; Type: CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image_to_image
    ADD CONSTRAINT image_to_image_pkey PRIMARY KEY (left_id, right_id);


--
-- Name: image image_gallery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image
    ADD CONSTRAINT image_gallery_id_fkey FOREIGN KEY (gallery_id) REFERENCES public.gallery(id);


--
-- Name: image_to_image image_to_image_left_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image_to_image
    ADD CONSTRAINT image_to_image_left_id_fkey FOREIGN KEY (left_id) REFERENCES public.image(id);


--
-- Name: image_to_image image_to_image_right_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mgallery
--

ALTER TABLE ONLY public.image_to_image
    ADD CONSTRAINT image_to_image_right_id_fkey FOREIGN KEY (right_id) REFERENCES public.image(id);


--
-- PostgreSQL database dump complete
--

