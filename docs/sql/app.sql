/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.1.160-13306
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : 192.168.1.160:13306
 Source Schema         : app

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 29/11/2025 18:44:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cms_category
-- ----------------------------
DROP TABLE IF EXISTS `cms_category`;
CREATE TABLE `cms_category`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `site_id` bigint(0) NULL DEFAULT 0 COMMENT '站点id',
  `parent_id` bigint(0) NULL DEFAULT 0 COMMENT '父id',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '栏目名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '简介',
  `seo_keywords` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'seo关键字',
  `seo_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'seo描述',
  `img` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '大图',
  `model_id` bigint(0) NULL DEFAULT 0 COMMENT '内容模型id',
  `category_model_id` bigint(0) NULL DEFAULT 0 COMMENT '栏目模型id',
  `is_page` tinyint(1) NULL DEFAULT 0 COMMENT '是否单页面',
  `is_show` tinyint(1) NULL DEFAULT 1 COMMENT '是否显示',
  `sort` bigint(0) NULL DEFAULT 10 COMMENT '排序',
  `category_template` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '栏目首页模板',
  `list_template` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '栏目列表模板',
  `show_template` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '栏目详情页模板',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '栏目' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_category
-- ----------------------------

-- ----------------------------
-- Table structure for cms_category_ext
-- ----------------------------
DROP TABLE IF EXISTS `cms_category_ext`;
CREATE TABLE `cms_category_ext`  (
  `category_id` bigint(0) NOT NULL COMMENT '栏目id',
  `ext1` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段1',
  `ext2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段2',
  `ext3` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段3',
  `ext4` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段4',
  `ext5` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段5',
  PRIMARY KEY (`category_id`) USING BTREE,
  UNIQUE INDEX `idx_category_ext_cate_id`(`category_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'r_栏目扩展' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_category_ext
-- ----------------------------

-- ----------------------------
-- Table structure for cms_content
-- ----------------------------
DROP TABLE IF EXISTS `cms_content`;
CREATE TABLE `cms_content`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `category_id` bigint(0) NOT NULL COMMENT '所属栏目',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `author` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '作者',
  `source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源',
  `seo_keywords` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'seo关键字',
  `seo_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'seo描述',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '摘要',
  `sort` bigint(0) NULL DEFAULT 10 COMMENT '排序',
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '单图',
  `images` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '多图',
  `is_recommend` tinyint(1) NULL DEFAULT 1 COMMENT '是否推荐',
  `is_published` tinyint(1) NULL DEFAULT 0 COMMENT '是否发布',
  `publish_time` datetime(3) NULL DEFAULT NULL COMMENT '发布时间',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '内容',
  `status` int(0) NULL DEFAULT NULL COMMENT '业务状态',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_cms_content_cate_id`(`category_id`) USING BTREE,
  INDEX `idx_cms_content_title`(`title`) USING BTREE,
  INDEX `idx_cms_content_publishtime`(`publish_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '内容' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_content
-- ----------------------------

-- ----------------------------
-- Table structure for cms_content_ext
-- ----------------------------
DROP TABLE IF EXISTS `cms_content_ext`;
CREATE TABLE `cms_content_ext`  (
  `content_id` bigint(0) NOT NULL COMMENT '内容id',
  `ext1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段1',
  `ext2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段2',
  `ext3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段3',
  `ext4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段4',
  `ext5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展字段5',
  PRIMARY KEY (`content_id`) USING BTREE,
  UNIQUE INDEX `idx_content_ext_content_id`(`content_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'r_内容扩展' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_content_ext
-- ----------------------------

-- ----------------------------
-- Table structure for cms_content_pos
-- ----------------------------
DROP TABLE IF EXISTS `cms_content_pos`;
CREATE TABLE `cms_content_pos`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `content_id` bigint(0) NULL DEFAULT NULL COMMENT '内容id',
  `position_id` bigint(0) NULL DEFAULT NULL COMMENT '推荐位id',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_cms_content_pos_conid`(`content_id`) USING BTREE,
  INDEX `idx_cms_content_pos_posid`(`position_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'r_内容推荐位' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_content_pos
-- ----------------------------

-- ----------------------------
-- Table structure for cms_model
-- ----------------------------
DROP TABLE IF EXISTS `cms_model`;
CREATE TABLE `cms_model`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `site_id` bigint(0) NULL DEFAULT 0 COMMENT '站点id',
  `model_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型名称',
  `table_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '模型表',
  `model_type` int(0) NULL DEFAULT NULL COMMENT '模型类型(1->内容模型|CONTENT,2->栏目模型|CATEGORY)',
  `category_template` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '栏目首页模板',
  `list_template` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '栏目列表页模板',
  `show_template` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '栏目详情页模板',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '模型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_model
-- ----------------------------

-- ----------------------------
-- Table structure for cms_page
-- ----------------------------
DROP TABLE IF EXISTS `cms_page`;
CREATE TABLE `cms_page`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `category_id` bigint(0) NOT NULL COMMENT '栏目id',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '内容',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_cms_page_category_id`(`category_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '单页面' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_page
-- ----------------------------

-- ----------------------------
-- Table structure for cms_position
-- ----------------------------
DROP TABLE IF EXISTS `cms_position`;
CREATE TABLE `cms_position`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `logo` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图标',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '推荐位' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_position
-- ----------------------------

-- ----------------------------
-- Table structure for cms_site
-- ----------------------------
DROP TABLE IF EXISTS `cms_site`;
CREATE TABLE `cms_site`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `site_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '站点名称',
  `site_keywords` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '站点关键字',
  `site_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '站点描述',
  `site_logo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '站点logo',
  `domain` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '绑定域名',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '站点' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_site
-- ----------------------------

-- ----------------------------
-- Table structure for cms_slide
-- ----------------------------
DROP TABLE IF EXISTS `cms_slide`;
CREATE TABLE `cms_slide`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `site_id` bigint(0) NULL DEFAULT 0 COMMENT '站点id',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '幻灯片分类',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '分类备注',
  `is_show` tinyint(1) NULL DEFAULT 1 COMMENT '是否显示',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '幻灯片' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_slide
-- ----------------------------

-- ----------------------------
-- Table structure for cms_slide_item
-- ----------------------------
DROP TABLE IF EXISTS `cms_slide_item`;
CREATE TABLE `cms_slide_item`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `slide_id` bigint(0) NULL DEFAULT NULL COMMENT '幻灯片id',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '幻灯片名称',
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '幻灯片图片',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '幻灯片链接',
  `target` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '打开方式',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '幻灯片描述',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '幻灯片内容',
  `is_show` tinyint(1) NULL DEFAULT 1 COMMENT '是否显示',
  `sort` bigint(0) NULL DEFAULT 10 COMMENT '排序',
  `ext` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '扩展信息',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '幻灯片子项' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_slide_item
-- ----------------------------

-- ----------------------------
-- Table structure for cms_view_click
-- ----------------------------
DROP TABLE IF EXISTS `cms_view_click`;
CREATE TABLE `cms_view_click`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `view_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '页面类型(home->首页,category->栏目首页,list->栏目列表页,page->单页面,show->详情页)',
  `category_id` bigint(0) NULL DEFAULT NULL COMMENT '栏目id',
  `content_id` bigint(0) NULL DEFAULT NULL COMMENT '内容id',
  `page_view` int(0) NOT NULL DEFAULT 1 COMMENT '页面访问量',
  `status` int(0) NULL DEFAULT NULL COMMENT '业务状态',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '修改人',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '修改时间',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_cms_view_click_type`(`view_type`) USING BTREE,
  INDEX `idx_cms_view_click_cate_id`(`category_id`) USING BTREE,
  INDEX `idx_cms_view_click_con_id`(`content_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '页面访问量' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cms_view_click
-- ----------------------------

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`  (
  `id` bigint(0) NOT NULL COMMENT '配置ID',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `group_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分组编码',
  `content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '配置内容',
  `is_sys` tinyint(1) NULL DEFAULT 0 COMMENT '是否系统',
  `enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_config_code`(`code`) USING BTREE,
  INDEX `idx_config_group_code`(`group_code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_config
-- ----------------------------
INSERT INTO `sys_config` VALUES (1763451288845385730, '登录图片验证码是否启用标识', 'MOLE_CAPTCHA_OPEN', 'default', 'false', 1, 1, NULL, '2024-03-01 14:28:45.259', 1567738052492341249, '2025-07-06 18:55:32.665', 1567738052492341249, 0);
INSERT INTO `sys_config` VALUES (1898707669169819649, '图片服务器baseurl', 'IMG_BASE_URL', 'default', 'http://127.0.0.1:8080/uploadfiles/', 1, 1, NULL, '2025-03-09 07:09:19.269', 1, '2025-03-12 10:51:22.702', 1, 0);
INSERT INTO `sys_config` VALUES (1898729104307216386, '默认密码', 'DEFAULT_PASSWORD', 'default', '123456', 1, 1, NULL, '2025-03-09 08:34:29.805', 1, '2025-03-11 08:42:31.854', 1, 0);

-- ----------------------------
-- Table structure for sys_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept`  (
  `id` bigint(0) NOT NULL COMMENT '部门ID',
  `parent_id` bigint(0) NULL DEFAULT 0 COMMENT '父ID',
  `pids` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '父ID集合',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '部门名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `sort` bigint(0) NULL DEFAULT 999 COMMENT '排序',
  `enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `leader_ids` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '部门负责人ID集合',
  `main_leader_id` bigint(0) NULL DEFAULT NULL COMMENT '分管领导ID',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_sys_dept_code`(`code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '部门' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dept
-- ----------------------------
INSERT INTO `sys_dept` VALUES (1, 0, '0', '研发部', 'yanfabu', 999, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (1895112980235673601, 0, NULL, '财务部', 'caiwubu', 1, 1, '1,2', 2, NULL, '2025-02-27 08:05:18.642', 1, '2025-02-27 09:05:44.509', 1, 0);
INSERT INTO `sys_dept` VALUES (1895120231465816066, 0, NULL, '集团公司', 'jituan', 22, 1, '1,2,3', 1583687667914043393, NULL, '2025-02-27 08:34:07.470', 1, '2025-02-27 09:06:02.994', 1, 0);
INSERT INTO `sys_dept` VALUES (1895120305528836098, 1895120231465816066, NULL, '子公司', 'zigongsi', 222, 1, NULL, 2, NULL, '2025-02-27 08:34:25.129', 1, '2025-02-27 08:34:25.129', 1, 0);

-- ----------------------------
-- Table structure for sys_dict
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict`;
CREATE TABLE `sys_dict`  (
  `id` bigint(0) NOT NULL COMMENT '字典ID',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '字典名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `group_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分组编码',
  `sort` bigint(0) NULL DEFAULT 999 COMMENT '排序',
  `enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `data_type` int(0) NULL DEFAULT 1 COMMENT '数据类型（1：字符串；2：整型）',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_dict_code`(`code`) USING BTREE,
  INDEX `idx_dict_group_code`(`group_code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '字典' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict
-- ----------------------------
INSERT INTO `sys_dict` VALUES (1858024553577254913, '性别', 'sex', 'sys', 6, 0, 2, NULL, '2024-11-16 23:49:08.656', 1, '2024-11-17 01:31:11.544', 1, 0);
INSERT INTO `sys_dict` VALUES (1858027332748234754, '是否', 'yes_no', 'sys', 2, 0, 2, NULL, '2024-11-17 00:00:11.262', 1, '2024-11-17 01:31:04.644', 1, 0);
INSERT INTO `sys_dict` VALUES (1858033037337243650, '字典分组', 'sys_dict_group_code', 'default', 3, 1, 1, NULL, '2024-11-17 00:22:51.343', 1, '2024-11-17 00:24:10.835', 1, 0);
INSERT INTO `sys_dict` VALUES (1858033427336212482, '数据类型', 'sys_dict_data_type', 'sys', 1, 0, 2, NULL, '2024-11-17 00:24:24.330', 1, '2024-11-17 01:30:19.016', 1, 0);
INSERT INTO `sys_dict` VALUES (1868678995255287809, '系统配置分组', 'sys_config_group_code', 'sys', 2, 1, 1, NULL, '2024-12-16 09:26:05.502', 1, '2024-12-16 09:26:05.502', 1, 0);

-- ----------------------------
-- Table structure for sys_dict_item
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_item`;
CREATE TABLE `sys_dict_item`  (
  `id` bigint(0) NOT NULL COMMENT '字典项ID',
  `dict_id` bigint(0) NOT NULL COMMENT '字典ID',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '字典项名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `sort` bigint(0) NULL DEFAULT 999 COMMENT '排序',
  `enabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_dict_item_dict_id`(`dict_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '字典项' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_item
-- ----------------------------
INSERT INTO `sys_dict_item` VALUES (1858025187047198722, 1858024553577254913, '男', '1', 1, 1, NULL, '2024-11-16 23:51:39.688', 1, '2024-11-16 23:51:39.688', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858025222853971969, 1858024553577254913, '女', '2', 2, 1, NULL, '2024-11-16 23:51:48.232', 1, '2024-11-16 23:51:48.232', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858025259147284481, 1858024553577254913, '未知', '3', 3, 1, NULL, '2024-11-16 23:51:56.881', 1, '2024-11-16 23:51:56.881', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858027710306910209, 1858027332748234754, '是', '1', 1, 1, NULL, '2024-11-17 00:01:41.280', 1, '2024-11-17 00:01:41.280', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858027750832275457, 1858027332748234754, '否', '0', 20, 1, NULL, '2024-11-17 00:01:50.946', 1, '2024-11-17 00:09:48.562', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858033116425039873, 1858033037337243650, '默认分组', 'default', 1, 1, NULL, '2024-11-17 00:23:10.204', 1, '2024-11-17 00:23:10.204', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858033490091388930, 1858033427336212482, '字符串', '1', 1, 1, NULL, '2024-11-17 00:24:39.299', 1, '2024-11-17 00:24:54.081', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858033526124654593, 1858033427336212482, '整型', '2', 2, 1, NULL, '2024-11-17 00:24:47.879', 1, '2024-11-17 00:24:47.879', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1858049956740136961, 1858033037337243650, '系统管理', 'sys', 2, 1, '系统管理模块相关的字典', '2024-11-17 01:30:05.242', 1, '2024-11-17 01:30:05.242', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1868679066994663425, 1868678995255287809, '默认分组', 'default', 1, 1, NULL, '2024-12-16 09:26:22.614', 1, '2024-12-16 09:26:22.614', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1868679183579537410, 1868678995255287809, '支付宝支付', 'ali_pay_config', 2, 1, NULL, '2024-12-16 09:26:50.411', 1, '2024-12-16 09:27:17.419', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1868679274512048130, 1868678995255287809, '微信支付', 'wx_pay', 999, 1, NULL, '2024-12-16 09:27:12.083', 1, '2024-12-16 09:27:12.083', 1, 0);
INSERT INTO `sys_dict_item` VALUES (1868679380103651330, 1868678995255287809, '七牛云存储', 'qinniu_oss', 999, 1, NULL, '2024-12-16 09:27:37.268', 1, '2024-12-16 09:27:37.268', 1, 0);

-- ----------------------------
-- Table structure for sys_file_info
-- ----------------------------
DROP TABLE IF EXISTS `sys_file_info`;
CREATE TABLE `sys_file_info`  (
  `id` bigint(0) NOT NULL COMMENT '文件信息ID',
  `url` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件访问地址',
  `size` bigint(0) NULL DEFAULT NULL COMMENT '文件大小，单位字节',
  `size_info` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件大小，有单位',
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名称',
  `original_filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始文件名',
  `base_path` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '基础存储路径',
  `path` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '存储路径',
  `ext` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件扩展名',
  `content_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'MIME类型',
  `platform` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '存储平台',
  `th_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '缩略图访问路径',
  `th_filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '缩略图大小，单位字节',
  `th_size` bigint(0) NULL DEFAULT NULL COMMENT '缩略图大小，单位字节',
  `th_size_info` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '缩略图大小，有单位',
  `th_content_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '缩略图MIME类型',
  `object_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件所属对象id',
  `object_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件所属对象类型，例如用户头像，评价图片',
  `attr` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附加属性',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文件信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_file_info
-- ----------------------------
INSERT INTO `sys_file_info` VALUES (1899850779719409665, 'mldong/default/202503/67d1ad8a49d08f36b9ef7cc8.jpg', 59340, '57.95 KB', '67d1ad8a49d08f36b9ef7cc8.jpg', 'ai.jpg', 'mldong/', 'default/202503/', 'jpg', 'image/jpeg', 'local-plus-1', NULL, NULL, NULL, NULL, NULL, '1899850779719409665', NULL, '{\"bizType\":\"default\",\"persist\":1}', '2025-03-12 10:51:38.072', 1, '2025-03-12 10:51:38.522', 1);

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `id` bigint(0) NOT NULL COMMENT '菜单ID',
  `app_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '应用编码',
  `parent_id` bigint(0) NOT NULL DEFAULT 0 COMMENT '父ID',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `pids` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '父ID集合',
  `type` int(0) NULL DEFAULT NULL COMMENT '菜单类型<sys_menu_type>',
  `sort` bigint(0) NULL DEFAULT 999 COMMENT '排序',
  `path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '路由地址',
  `component` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '组件地址',
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `is_show` tinyint(1) NULL DEFAULT 1 COMMENT '是否显示',
  `is_link` tinyint(1) NULL DEFAULT NULL COMMENT '是否链接',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '外部链接地址',
  `enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `open_type` int(0) NULL DEFAULT NULL COMMENT '打开方式<sys_menu_open_type>',
  `is_cache` tinyint(1) NULL DEFAULT NULL COMMENT '是否缓存',
  `is_sync` tinyint(1) NULL DEFAULT 1 COMMENT '是否同步',
  `variable` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '额外参数JSON',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_sys_menu_code`(`code`) USING BTREE,
  INDEX `idx_sys_menu_app_code`(`app_code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '菜单' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (2206080911290667008, 'platform', 0, 'page.dashboard.title', 'Dashboard', '0', 1, -1, '/dashboard', 'BasicLayout', 'lucide:layout-dashboard', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"BasicLayout\",\"icon\":\"lucide:layout-dashboard\",\"order\":-1,\"redirect\":\"/analytics\"}', '2025-07-12 21:57:56.253', NULL, '2025-07-12 21:58:03.176', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911307444224, 'platform', 2206080911290667008, 'page.dashboard.analytics', 'Analytics', '0,2206080911290667008', 2, 999, '/analytics', '/dashboard/analytics/index', 'lucide:area-chart', 1, 0, NULL, 1, 1, 1, 1, '{\"affixTab\":true,\"component\":\"/dashboard/analytics/index\",\"icon\":\"lucide:area-chart\"}', '2025-07-12 21:57:56.257', NULL, '2025-07-12 21:58:03.180', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911320027136, 'platform', 2206080911290667008, 'page.dashboard.workspace', 'Workspace', '0,2206080911290667008', 2, 999, '/workspace', '/dashboard/workspace/index', 'carbon:workspace', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"/dashboard/workspace/index\",\"icon\":\"carbon:workspace\"}', '2025-07-12 21:57:56.261', NULL, '2025-07-12 21:58:03.184', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911336804352, 'platform', 0, 'demos.title', 'Demos', '0', 1, 1000, '/demos', 'BasicLayout', 'ic:baseline-view-in-ar', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"BasicLayout\",\"icon\":\"ic:baseline-view-in-ar\",\"keepAlive\":true,\"order\":1000,\"redirect\":\"/demos/ant-design\"}', '2025-07-12 21:57:56.265', NULL, '2025-07-12 21:58:03.187', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911353581568, 'platform', 2206080911336804352, 'demos.antd', 'AntDesignDemos', '0,2206080911336804352', 2, 999, '/demos/ant-design', '/demos/antd/index', '', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"/demos/antd/index\"}', '2025-07-12 21:57:56.269', NULL, '2025-07-12 21:58:03.193', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911370358784, 'platform', 0, '系统设置', 'sys:manager', '0', 1, 1000, '/sys/manager', 'BasicLayout', 'ant-design:setting-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"BasicLayout\",\"icon\":\"ant-design:setting-outlined\",\"keepAlive\":true,\"order\":1000,\"perms\":[\"admin\",\"sys:manager\"],\"redirect\":\"/sys/user/index\"}', '2025-07-12 21:57:56.272', NULL, '2025-07-12 21:58:03.196', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911378747392, 'platform', 2206080911370358784, '用户管理', 'sys:user', '0,2206080911370358784', 2, 10, '/sys/user/index', '/sys/user/index', 'ant-design:user-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:playUser\":\"扮演用户\",\"sys:user:detail\":\"查看用户详情\",\"sys:user:grantRole\":\"授权角色\",\"sys:user:locked\":\"锁定用户\",\"sys:user:page\":\"分页查询用户\",\"sys:user:remove\":\"删除用户\",\"sys:user:resetPassword\":\"重置密码\",\"sys:user:save\":\"添加用户\",\"sys:user:unLocked\":\"取消锁定\",\"sys:user:update\":\"修改用户\"},\"component\":\"/sys/user/index\",\"icon\":\"ant-design:user-outlined\",\"order\":10,\"perms\":[\"admin\",\"sys:user\"]}', '2025-07-12 21:57:56.274', NULL, '2025-07-12 21:58:03.198', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911387136000, 'platform', 2206080911378747392, '分页查询用户', 'sys:user:page', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.277', NULL, '2025-07-12 21:58:03.200', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911395524608, 'platform', 2206080911378747392, '查看用户详情', 'sys:user:detail', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.278', NULL, '2025-07-12 21:58:03.202', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911403913216, 'platform', 2206080911378747392, '添加用户', 'sys:user:save', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.280', NULL, '2025-07-12 21:58:03.205', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911416496128, 'platform', 2206080911378747392, '修改用户', 'sys:user:update', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.283', NULL, '2025-07-12 21:58:03.208', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911429079040, 'platform', 2206080911378747392, '删除用户', 'sys:user:remove', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.286', NULL, '2025-07-12 21:58:03.211', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911441661952, 'platform', 2206080911378747392, '扮演用户', 'sys:playUser', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.289', NULL, '2025-07-12 21:58:03.214', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911450050560, 'platform', 2206080911378747392, '重置密码', 'sys:user:resetPassword', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.292', NULL, '2025-07-12 21:58:03.216', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911462633472, 'platform', 2206080911378747392, '授权角色', 'sys:user:grantRole', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.295', NULL, '2025-07-12 21:58:03.218', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911471022080, 'platform', 2206080911378747392, '锁定用户', 'sys:user:locked', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.297', NULL, '2025-07-12 21:58:03.221', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911479410688, 'platform', 2206080911378747392, '取消锁定', 'sys:user:unLocked', '0,2206080911370358784,2206080911378747392', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.298', NULL, '2025-07-12 21:58:03.223', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911487799296, 'platform', 2206080911370358784, '在线用户', 'sys:user:onlineUserList', '0,2206080911370358784', 2, 15, '/sys/user/online-user-list', '/sys/user/online-user-list', 'ant-design:cloud-server-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"btn:onlineUser:detail\":\"在线用户详情\",\"sys:user:kickoutByLoginId\":\"将用户踢下线\",\"sys:user:kickoutByTokenValue\":\"将Token凭证踢下线\",\"sys:user:logoutByLoginId\":\"强制注销用户\",\"sys:user:logoutByTokenValue\":\"强制注销Token凭证\"},\"component\":\"/sys/user/online-user-list\",\"icon\":\"ant-design:cloud-server-outlined\",\"order\":15,\"perms\":[\"admin\",\"sys:user:onlineUserList\"]}', '2025-07-12 21:57:56.301', NULL, '2025-07-12 21:58:03.226', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911504576512, 'platform', 2206080911487799296, '在线用户详情', 'btn:onlineUser:detail', '0,2206080911370358784,2206080911487799296', 3, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.304', NULL, '2025-07-12 21:58:03.230', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911512965120, 'platform', 2206080911487799296, '强制注销用户', 'sys:user:logoutByLoginId', '0,2206080911370358784,2206080911487799296', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.307', NULL, '2025-07-12 21:58:03.232', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911521353728, 'platform', 2206080911487799296, '将用户踢下线', 'sys:user:kickoutByLoginId', '0,2206080911370358784,2206080911487799296', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.309', NULL, '2025-07-12 21:58:03.234', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911529742336, 'platform', 2206080911487799296, '强制注销Token凭证', 'sys:user:logoutByTokenValue', '0,2206080911370358784,2206080911487799296', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.311', NULL, '2025-07-12 21:58:03.237', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911538130944, 'platform', 2206080911487799296, '将Token凭证踢下线', 'sys:user:kickoutByTokenValue', '0,2206080911370358784,2206080911487799296', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.313', NULL, '2025-07-12 21:58:03.239', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911546519552, 'platform', 2206080911370358784, '角色管理', 'sys:role', '0,2206080911370358784', 2, 20, '/sys/role/index', '/sys/role/index', 'ant-design:team-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:rbac:removeUserRole\":\"成员管理（删除用户角色关系）\",\"sys:rbac:saveRoleMenu\":\"设置权限（保存角色菜单关系）\",\"sys:rbac:saveUserRole\":\"成员管理（添加用户角色关系）\",\"sys:rbac:userListByRoleId\":\"成员管理（通过角色ID获取用户列表）\",\"sys:rbac:userListExcludeRoleId\":\"成员管理（获取用户列表-排除指定角色）\",\"sys:role:detail\":\"查看角色详情\",\"sys:role:grantDataScope\":\"给角色授权数据权限\",\"sys:role:page\":\"分页查询角色\",\"sys:role:remove\":\"删除角色\",\"sys:role:save\":\"添加角色\",\"sys:role:update\":\"修改角色\"},\"component\":\"/sys/role/index\",\"icon\":\"ant-design:team-outlined\",\"order\":20,\"perms\":[\"admin\",\"sys:role\"]}', '2025-07-12 21:57:56.315', NULL, '2025-07-12 21:58:03.243', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911563296768, 'platform', 2206080911546519552, '分页查询角色', 'sys:role:page', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.319', NULL, '2025-07-12 21:58:03.245', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911575879680, 'platform', 2206080911546519552, '查看角色详情', 'sys:role:detail', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.322', NULL, '2025-07-12 21:58:03.247', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911588462592, 'platform', 2206080911546519552, '添加角色', 'sys:role:save', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.324', NULL, '2025-07-12 21:58:03.249', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911592656896, 'platform', 2206080911546519552, '修改角色', 'sys:role:update', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.326', NULL, '2025-07-12 21:58:03.252', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911601045504, 'platform', 2206080911546519552, '删除角色', 'sys:role:remove', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.328', NULL, '2025-07-12 21:58:03.253', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911609434112, 'platform', 2206080911546519552, '设置权限（保存角色菜单关系）', 'sys:rbac:saveRoleMenu', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.329', NULL, '2025-07-12 21:58:03.255', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911617822720, 'platform', 2206080911546519552, '成员管理（通过角色ID获取用户列表）', 'sys:rbac:userListByRoleId', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.331', NULL, '2025-07-12 21:58:03.259', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911626211328, 'platform', 2206080911546519552, '成员管理（添加用户角色关系）', 'sys:rbac:saveUserRole', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.334', NULL, '2025-07-12 21:58:03.261', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911642988544, 'platform', 2206080911546519552, '成员管理（获取用户列表-排除指定角色）', 'sys:rbac:userListExcludeRoleId', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.337', NULL, '2025-07-12 21:58:03.263', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911655571456, 'platform', 2206080911546519552, '成员管理（删除用户角色关系）', 'sys:rbac:removeUserRole', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.341', NULL, '2025-07-12 21:58:03.265', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911668154368, 'platform', 2206080911546519552, '给角色授权数据权限', 'sys:role:grantDataScope', '0,2206080911370358784,2206080911546519552', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.343', NULL, '2025-07-12 21:58:03.267', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911676542976, 'platform', 2206080911370358784, '菜单管理', 'sys:menu', '0,2206080911370358784', 2, 30, '/sys/menu/index', '/sys/menu/index', 'ant-design:menu-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:menu:detail\":\"查看菜单详情\",\"sys:menu:list\":\"菜单列表\",\"sys:menu:remove\":\"删除菜单\",\"sys:menu:save\":\"添加菜单\",\"sys:menu:tree\":\"菜单树\",\"sys:menu:update\":\"修改菜单\"},\"component\":\"/sys/menu/index\",\"icon\":\"ant-design:menu-outlined\",\"order\":30,\"perms\":[\"admin\",\"sys:menu\"]}', '2025-07-12 21:57:56.345', NULL, '2025-07-12 21:58:03.269', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911684931584, 'platform', 2206080911676542976, '菜单列表', 'sys:menu:list', '0,2206080911370358784,2206080911676542976', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.347', NULL, '2025-07-12 21:58:03.271', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911693320192, 'platform', 2206080911676542976, '菜单树', 'sys:menu:tree', '0,2206080911370358784,2206080911676542976', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.349', NULL, '2025-07-12 21:58:03.274', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911701708800, 'platform', 2206080911676542976, '查看菜单详情', 'sys:menu:detail', '0,2206080911370358784,2206080911676542976', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.352', NULL, '2025-07-12 21:58:03.277', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911714291712, 'platform', 2206080911676542976, '添加菜单', 'sys:menu:save', '0,2206080911370358784,2206080911676542976', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.355', NULL, '2025-07-12 21:58:03.279', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911726874624, 'platform', 2206080911676542976, '修改菜单', 'sys:menu:update', '0,2206080911370358784,2206080911676542976', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.357', NULL, '2025-07-12 21:58:03.282', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911739457536, 'platform', 2206080911676542976, '删除菜单', 'sys:menu:remove', '0,2206080911370358784,2206080911676542976', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.360', NULL, '2025-07-12 21:58:03.284', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911743651840, 'platform', 2206080911370358784, '前端路由', 'sys:routelist', '0,2206080911370358784', 2, 40, '/sys/menu/routelist', '/sys/menu/route-make-list', 'ant-design:ordered-list-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"btn:copy:antTreData\":\"复制AntTreeData\",\"btn:copy:idAndPidData\":\"复制id/pid数据\",\"btn:route:config\":\"查看路由配置\",\"sys:menu:syncRoute\":\"同步前端路由\"},\"component\":\"/sys/menu/route-make-list\",\"icon\":\"ant-design:ordered-list-outlined\",\"order\":40,\"perms\":[\"admin\",\"sys:routelist\"]}', '2025-07-12 21:57:56.362', NULL, '2025-07-12 21:58:03.286', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911756234752, 'platform', 2206080911743651840, '同步前端路由', 'sys:menu:syncRoute', '0,2206080911370358784,2206080911743651840', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.365', NULL, '2025-07-12 21:58:03.288', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911764623360, 'platform', 2206080911743651840, '查看路由配置', 'btn:route:config', '0,2206080911370358784,2206080911743651840', 3, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.366', NULL, '2025-07-12 21:58:03.291', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911777206272, 'platform', 2206080911743651840, '复制id/pid数据', 'btn:copy:idAndPidData', '0,2206080911370358784,2206080911743651840', 3, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.370', NULL, '2025-07-12 21:58:03.294', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911789789184, 'platform', 2206080911743651840, '复制AntTreeData', 'btn:copy:antTreData', '0,2206080911370358784,2206080911743651840', 3, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.372', NULL, '2025-07-12 21:58:03.296', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911798177792, 'platform', 2206080911370358784, '部门管理', 'sys:dept', '0,2206080911370358784', 2, 50, '/sys/dept/index', '/sys/dept/index', 'ant-design:deployment-unit-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:dept:autoSort\":\"自动排序\",\"sys:dept:detail\":\"查看部门详情\",\"sys:dept:list\":\"部门列表\",\"sys:dept:remove\":\"删除部门\",\"sys:dept:save\":\"添加部门\",\"sys:dept:tree\":\"部门树\",\"sys:dept:update\":\"修改部门\",\"sys:dept:updateSort\":\"更新排序\"},\"component\":\"/sys/dept/index\",\"icon\":\"ant-design:deployment-unit-outlined\",\"order\":50,\"perms\":[\"admin\",\"sys:dept\"]}', '2025-07-12 21:57:56.374', NULL, '2025-07-12 21:58:03.298', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911806566400, 'platform', 2206080911798177792, '部门列表', 'sys:dept:list', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.377', NULL, '2025-07-12 21:58:03.301', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911814955008, 'platform', 2206080911798177792, '部门树', 'sys:dept:tree', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.379', NULL, '2025-07-12 21:58:03.303', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911823343616, 'platform', 2206080911798177792, '查看部门详情', 'sys:dept:detail', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.380', NULL, '2025-07-12 21:58:03.306', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911831732224, 'platform', 2206080911798177792, '添加部门', 'sys:dept:save', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.383', NULL, '2025-07-12 21:58:03.310', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911844315136, 'platform', 2206080911798177792, '修改部门', 'sys:dept:update', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.385', NULL, '2025-07-12 21:58:03.312', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911856898048, 'platform', 2206080911798177792, '删除部门', 'sys:dept:remove', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.388', NULL, '2025-07-12 21:58:03.316', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911865286656, 'platform', 2206080911798177792, '自动排序', 'sys:dept:autoSort', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.390', NULL, '2025-07-12 21:58:03.318', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911873675264, 'platform', 2206080911798177792, '更新排序', 'sys:dept:updateSort', '0,2206080911370358784,2206080911798177792', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.393', NULL, '2025-07-12 21:58:03.321', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911882063872, 'platform', 2206080911370358784, '岗位管理', 'sys:post', '0,2206080911370358784', 2, 60, '/sys/post/index', '/sys/post/index', 'ant-design:share-alt-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:post:detail\":\"查看岗位详情\",\"sys:post:page\":\"分页查询岗位\",\"sys:post:remove\":\"删除岗位\",\"sys:post:save\":\"添加岗位\",\"sys:post:update\":\"修改岗位\"},\"component\":\"/sys/post/index\",\"icon\":\"ant-design:share-alt-outlined\",\"order\":60,\"perms\":[\"admin\",\"sys:post\"]}', '2025-07-12 21:57:56.395', NULL, '2025-07-12 21:58:03.324', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911894646784, 'platform', 2206080911882063872, '分页查询岗位', 'sys:post:page', '0,2206080911370358784,2206080911882063872', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.397', NULL, '2025-07-12 21:58:03.328', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911903035392, 'platform', 2206080911882063872, '查看岗位详情', 'sys:post:detail', '0,2206080911370358784,2206080911882063872', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.400', NULL, '2025-07-12 21:58:03.329', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911919812608, 'platform', 2206080911882063872, '添加岗位', 'sys:post:save', '0,2206080911370358784,2206080911882063872', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.404', NULL, '2025-07-12 21:58:03.332', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911928201216, 'platform', 2206080911882063872, '修改岗位', 'sys:post:update', '0,2206080911370358784,2206080911882063872', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.406', NULL, '2025-07-12 21:58:03.334', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911936589824, 'platform', 2206080911882063872, '删除岗位', 'sys:post:remove', '0,2206080911370358784,2206080911882063872', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.408', NULL, '2025-07-12 21:58:03.336', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911949172736, 'platform', 2206080911370358784, '数据字典', 'sys:dict', '0,2206080911370358784', 2, 70, '/sys/dict/index', '/sys/dict/index', 'ant-design:database-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:dict:clearCache\":\"清空字典缓存\",\"sys:dict:customDictList\":\"自定义字典列表\",\"sys:dict:detail\":\"查看参数字典\",\"sys:dict:enumDictList\":\"枚举字典列表\",\"sys:dict:page\":\"分页查询字典\",\"sys:dict:remove\":\"删除字典\",\"sys:dict:save\":\"添加字典\",\"sys:dict:update\":\"修改字典\",\"sys:dictItem:detail\":\"查看参数字典项\",\"sys:dictItem:page\":\"分页查询字典项\",\"sys:dictItem:remove\":\"删除字典项\",\"sys:dictItem:save\":\"添加字典项\",\"sys:dictItem:update\":\"修改字典项\"},\"component\":\"/sys/dict/index\",\"icon\":\"ant-design:database-outlined\",\"order\":70,\"perms\":[\"admin\",\"sys:dict\"]}', '2025-07-12 21:57:56.411', NULL, '2025-07-12 21:58:03.339', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911957561344, 'platform', 2206080911949172736, '分页查询字典', 'sys:dict:page', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.413', NULL, '2025-07-12 21:58:03.342', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911965949952, 'platform', 2206080911949172736, '查看参数字典', 'sys:dict:detail', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.415', NULL, '2025-07-12 21:58:03.346', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911974338560, 'platform', 2206080911949172736, '添加字典', 'sys:dict:save', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.417', NULL, '2025-07-12 21:58:03.348', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080911991115776, 'platform', 2206080911949172736, '修改字典', 'sys:dict:update', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.420', NULL, '2025-07-12 21:58:03.350', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912003698688, 'platform', 2206080911949172736, '删除字典', 'sys:dict:remove', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.423', NULL, '2025-07-12 21:58:03.352', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912012087296, 'platform', 2206080911949172736, '分页查询字典项', 'sys:dictItem:page', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.425', NULL, '2025-07-12 21:58:03.354', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912020475904, 'platform', 2206080911949172736, '查看参数字典项', 'sys:dictItem:detail', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.428', NULL, '2025-07-12 21:58:03.357', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912028864512, 'platform', 2206080911949172736, '添加字典项', 'sys:dictItem:save', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.430', NULL, '2025-07-12 21:58:03.361', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912037253120, 'platform', 2206080911949172736, '修改字典项', 'sys:dictItem:update', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.432', NULL, '2025-07-12 21:58:03.364', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912045641728, 'platform', 2206080911949172736, '删除字典项', 'sys:dictItem:remove', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.434', NULL, '2025-07-12 21:58:03.366', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912062418944, 'platform', 2206080911949172736, '枚举字典列表', 'sys:dict:enumDictList', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.437', NULL, '2025-07-12 21:58:03.369', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912070807552, 'platform', 2206080911949172736, '自定义字典列表', 'sys:dict:customDictList', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.439', NULL, '2025-07-12 21:58:03.371', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912083390464, 'platform', 2206080911949172736, '清空字典缓存', 'sys:dict:clearCache', '0,2206080911370358784,2206080911949172736', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.443', NULL, '2025-07-12 21:58:03.374', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912095973376, 'platform', 2206080911370358784, '参数配置', 'sys:config', '0,2206080911370358784', 2, 80, '/sys/config/index', '/sys/config/index', 'ant-design:file-text-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:config:detail\":\"查看参数配置详情\",\"sys:config:page\":\"分页查询参数配置\",\"sys:config:remove\":\"删除参数配置\",\"sys:config:save\":\"添加参数配置\",\"sys:config:update\":\"修改参数配置\"},\"component\":\"/sys/config/index\",\"icon\":\"ant-design:file-text-outlined\",\"order\":80,\"perms\":[\"admin\",\"sys:config\"]}', '2025-07-12 21:57:56.446', NULL, '2025-07-12 21:58:03.377', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912108556288, 'platform', 2206080912095973376, '分页查询参数配置', 'sys:config:page', '0,2206080911370358784,2206080912095973376', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.448', NULL, '2025-07-12 21:58:03.379', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912116944896, 'platform', 2206080912095973376, '查看参数配置详情', 'sys:config:detail', '0,2206080911370358784,2206080912095973376', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.451', NULL, '2025-07-12 21:58:03.382', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912129527808, 'platform', 2206080912095973376, '添加参数配置', 'sys:config:save', '0,2206080911370358784,2206080912095973376', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.454', NULL, '2025-07-12 21:58:03.384', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912146305024, 'platform', 2206080912095973376, '修改参数配置', 'sys:config:update', '0,2206080911370358784,2206080912095973376', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.458', NULL, '2025-07-12 21:58:03.386', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912163082240, 'platform', 2206080912095973376, '删除参数配置', 'sys:config:remove', '0,2206080911370358784,2206080912095973376', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.461', NULL, '2025-07-12 21:58:03.388', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912171470848, 'platform', 2206080911370358784, '定时任务', 'sys:timer', '0,2206080911370358784', 2, 90, '/sys/timer/index', '/sys/timer/index', 'ant-design:field-time-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"sys:timer:detail\":\"查看定时任务详情\",\"sys:timer:executeImmediate\":\"立即执行\",\"sys:timer:page\":\"分页查询定时任务\",\"sys:timer:reset\":\"重置定时任务\",\"sys:timer:start\":\"启动定时任务\",\"sys:timer:stop\":\"停止定时任务\",\"sys:timer:update\":\"修改定时任务\"},\"component\":\"/sys/timer/index\",\"icon\":\"ant-design:field-time-outlined\",\"order\":90,\"perms\":[\"admin\",\"sys:timer\"]}', '2025-07-12 21:57:56.464', NULL, '2025-07-12 21:58:03.391', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912179859456, 'platform', 2206080912171470848, '分页查询定时任务', 'sys:timer:page', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.466', NULL, '2025-07-12 21:58:03.394', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912196636672, 'platform', 2206080912171470848, '查看定时任务详情', 'sys:timer:detail', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.469', NULL, '2025-07-12 21:58:03.396', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912209219584, 'platform', 2206080912171470848, '修改定时任务', 'sys:timer:update', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.472', NULL, '2025-07-12 21:58:03.399', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912221802496, 'platform', 2206080912171470848, '停止定时任务', 'sys:timer:stop', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.476', NULL, '2025-07-12 21:58:03.400', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912230191104, 'platform', 2206080912171470848, '启动定时任务', 'sys:timer:start', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.478', NULL, '2025-07-12 21:58:03.402', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912238579712, 'platform', 2206080912171470848, '重置定时任务', 'sys:timer:reset', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.480', NULL, '2025-07-12 21:58:03.405', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912246968320, 'platform', 2206080912171470848, '立即执行', 'sys:timer:executeImmediate', '0,2206080911370358784,2206080912171470848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.482', NULL, '2025-07-12 21:58:03.408', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912255356928, 'platform', 0, '在线开发', 'dev:manager', '0', 1, 1010, '/dev/manager', 'BasicLayout', 'ant-design:cloud-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"BasicLayout\",\"icon\":\"ant-design:cloud-outlined\",\"keepAlive\":true,\"order\":1010,\"perms\":[\"admin\",\"dev:manager\"],\"redirect\":\"/dev/schema-group/index\"}', '2025-07-12 21:57:56.484', NULL, '2025-07-12 21:58:03.411', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912267939840, 'platform', 2206080912255356928, '模型分组', 'dev:schemaGroup', '0,2206080912255356928', 2, 10, '/dev/schema-group/index', '/dev/schema-group/index', 'ant-design:group-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"dev:schemaGroup:detail\":\"查看模型分组详情\",\"dev:schemaGroup:page\":\"分页查询模型分组\",\"dev:schemaGroup:remove\":\"删除模型分组\",\"dev:schemaGroup:save\":\"添加模型分组\",\"dev:schemaGroup:update\":\"修改模型分组\"},\"component\":\"/dev/schema-group/index\",\"icon\":\"ant-design:group-outlined\",\"order\":10,\"perms\":[\"admin\",\"dev:schemaGroup\"]}', '2025-07-12 21:57:56.487', NULL, '2025-07-12 21:58:03.414', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912280522752, 'platform', 2206080912267939840, '分页查询模型分组', 'dev:schemaGroup:page', '0,2206080912255356928,2206080912267939840', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.490', NULL, '2025-07-12 21:58:03.416', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912293105664, 'platform', 2206080912267939840, '查看模型分组详情', 'dev:schemaGroup:detail', '0,2206080912255356928,2206080912267939840', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.493', NULL, '2025-07-12 21:58:03.418', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912301494272, 'platform', 2206080912267939840, '添加模型分组', 'dev:schemaGroup:save', '0,2206080912255356928,2206080912267939840', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.495', NULL, '2025-07-12 21:58:03.420', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912314077184, 'platform', 2206080912267939840, '修改模型分组', 'dev:schemaGroup:update', '0,2206080912255356928,2206080912267939840', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.497', NULL, '2025-07-12 21:58:03.423', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912318271488, 'platform', 2206080912267939840, '删除模型分组', 'dev:schemaGroup:remove', '0,2206080912255356928,2206080912267939840', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.499', NULL, '2025-07-12 21:58:03.426', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912330854400, 'platform', 2206080912255356928, '数据模型', 'dev:schema', '0,2206080912255356928', 2, 20, '/dev/schema/index', '/dev/schema/index', 'ant-design:database-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"dev:schema:detail\":\"查看数据模型详情\",\"dev:schema:getByTableName\":\"查看元数据\",\"dev:schema:importTable\":\"导入数据库表\",\"dev:schema:page\":\"分页查询数据模型\",\"dev:schema:remove\":\"删除数据模型\",\"dev:schema:save\":\"添加数据模型\",\"dev:schema:update\":\"修改数据模型\",\"dev:schema:updateDesigner\":\"更新表单设计\",\"dev:schema:updateListKeys\":\"更新列表字段Key\",\"dev:schema:updateSearchFormKeys\":\"更新搜索表单字段Key\",\"dev:schemaField:detail\":\"查看模型字段详情\",\"dev:schemaField:page\":\"分页查询模型字段\",\"dev:schemaField:remove\":\"删除模型字段\",\"dev:schemaField:save\":\"添加模型字段\",\"dev:schemaField:update\":\"修改模型字段\",\"dev:schemaField:updateSort\":\"更新模型字段排序\"},\"component\":\"/dev/schema/index\",\"icon\":\"ant-design:database-outlined\",\"order\":20,\"perms\":[\"admin\",\"dev:schema\"]}', '2025-07-12 21:57:56.502', NULL, '2025-07-12 21:58:03.428', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912351825920, 'platform', 2206080912330854400, '分页查询数据模型', 'dev:schema:page', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.506', NULL, '2025-07-12 21:58:03.431', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912364408832, 'platform', 2206080912330854400, '查看数据模型详情', 'dev:schema:detail', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.509', NULL, '2025-07-12 21:58:03.433', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912372797440, 'platform', 2206080912330854400, '添加数据模型', 'dev:schema:save', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.511', NULL, '2025-07-12 21:58:03.436', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912376991744, 'platform', 2206080912330854400, '修改数据模型', 'dev:schema:update', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.513', NULL, '2025-07-12 21:58:03.439', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912389574656, 'platform', 2206080912330854400, '删除数据模型', 'dev:schema:remove', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.515', NULL, '2025-07-12 21:58:03.443', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912397963264, 'platform', 2206080912330854400, '导入数据库表', 'dev:schema:importTable', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.518', NULL, '2025-07-12 21:58:03.445', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912410546176, 'platform', 2206080912330854400, '查看元数据', 'dev:schema:getByTableName', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.520', NULL, '2025-07-12 21:58:03.447', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912465072128, 'platform', 2206080912330854400, '更新表单设计', 'dev:schema:updateDesigner', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.534', NULL, '2025-07-12 21:58:03.449', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912498626560, 'platform', 2206080912330854400, '分页查询模型字段', 'dev:schemaField:page', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.541', NULL, '2025-07-12 21:58:03.452', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912507015168, 'platform', 2206080912330854400, '查看模型字段详情', 'dev:schemaField:detail', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.544', NULL, '2025-07-12 21:58:03.454', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912519598080, 'platform', 2206080912330854400, '添加模型字段', 'dev:schemaField:save', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.546', NULL, '2025-07-12 21:58:03.457', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912527986688, 'platform', 2206080912330854400, '修改模型字段', 'dev:schemaField:update', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.548', NULL, '2025-07-12 21:58:03.460', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912536375296, 'platform', 2206080912330854400, '删除模型字段', 'dev:schemaField:remove', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.551', NULL, '2025-07-12 21:58:03.462', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912548958208, 'platform', 2206080912330854400, '更新模型字段排序', 'dev:schemaField:updateSort', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.554', NULL, '2025-07-12 21:58:03.465', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912565735424, 'platform', 2206080912330854400, '更新搜索表单字段Key', 'dev:schema:updateSearchFormKeys', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.557', NULL, '2025-07-12 21:58:03.467', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912574124032, 'platform', 2206080912330854400, '更新列表字段Key', 'dev:schema:updateListKeys', '0,2206080912255356928,2206080912330854400', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.560', NULL, '2025-07-12 21:58:03.469', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912582512640, 'platform', 0, '工作流程', 'wf:manager', '0', 1, 1010, '/wf/manager', 'BasicLayout', 'ant-design:laptop-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"BasicLayout\",\"icon\":\"ant-design:laptop-outlined\",\"keepAlive\":true,\"order\":1010,\"perms\":[\"admin\",\"wf:manager\"],\"redirect\":\"/wf/process-design/index\"}', '2025-07-12 21:57:56.562', NULL, '2025-07-12 21:58:03.471', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912595095552, 'platform', 2206080912582512640, '发起申请', 'wf:processDesign:listByType', '0,2206080912582512640', 2, 999, '/wf/process-instance/apply-list', '/wf/process-instance/apply-list', 'ion:grid-outline', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"/wf/process-instance/apply-list\",\"icon\":\"ion:grid-outline\",\"orderNo\":220,\"perms\":[\"admin\",\"wf:processDesign:listByType\"]}', '2025-07-12 21:57:56.564', NULL, '2025-07-12 21:58:03.474', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912603484160, 'platform', 2206080912582512640, '流程设计', 'wf:processDesign', '0,2206080912582512640', 2, 200, '/wf/process-design/index', '/wf/process-design/index', 'ant-design:book-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"wf:processDesign:deploy\":\"部署流程定义\",\"wf:processDesign:detail\":\"查看流程设计详情\",\"wf:processDesign:page\":\"分页查询流程设计\",\"wf:processDesign:redeploy\":\"重新部署流程定义\",\"wf:processDesign:remove\":\"删除流程设计\",\"wf:processDesign:save\":\"添加流程设计\",\"wf:processDesign:update\":\"修改流程设计\",\"wf:processDesign:updateDefine\":\"保存流程设计定义\"},\"component\":\"/wf/process-design/index\",\"icon\":\"ant-design:book-outlined\",\"order\":200,\"perms\":[\"admin\",\"wf:processDesign\"]}', '2025-07-12 21:57:56.566', NULL, '2025-07-12 21:58:03.478', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912620261376, 'platform', 2206080912603484160, '分页查询流程设计', 'wf:processDesign:page', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.570', NULL, '2025-07-12 21:58:03.481', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912628649984, 'platform', 2206080912603484160, '查看流程设计详情', 'wf:processDesign:detail', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.572', NULL, '2025-07-12 21:58:03.483', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912637038592, 'platform', 2206080912603484160, '添加流程设计', 'wf:processDesign:save', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.574', NULL, '2025-07-12 21:58:03.485', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912645427200, 'platform', 2206080912603484160, '修改流程设计', 'wf:processDesign:update', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.577', NULL, '2025-07-12 21:58:03.487', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912653815808, 'platform', 2206080912603484160, '删除流程设计', 'wf:processDesign:remove', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.578', NULL, '2025-07-12 21:58:03.489', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912662204416, 'platform', 2206080912603484160, '保存流程设计定义', 'wf:processDesign:updateDefine', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.581', NULL, '2025-07-12 21:58:03.511', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912670593024, 'platform', 2206080912603484160, '部署流程定义', 'wf:processDesign:deploy', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.582', NULL, '2025-07-12 21:58:03.542', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912683175936, 'platform', 2206080912603484160, '重新部署流程定义', 'wf:processDesign:redeploy', '0,2206080912582512640,2206080912603484160', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.586', NULL, '2025-07-12 21:58:03.546', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912695758848, 'platform', 2206080912582512640, '流程定义', 'wf:processDefine', '0,2206080912582512640', 2, 210, '/wf/process-define/index', '/wf/process-define/index', 'ant-design:picture-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"wf:processDefine:detail\":\"查看流程定义详情\",\"wf:processDefine:page\":\"分页查询流程定义\",\"wf:processDefine:remove\":\"删除流程定义\",\"wf:processDefine:startAndExecute\":\"发起流程\",\"wf:processDefine:upAndDown\":\"启用/禁用流程定义\"},\"component\":\"/wf/process-define/index\",\"icon\":\"ant-design:picture-outlined\",\"order\":210,\"perms\":[\"admin\",\"wf:processDefine\"]}', '2025-07-12 21:57:56.588', NULL, '2025-07-12 21:58:03.551', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912704147456, 'platform', 2206080912695758848, '分页查询流程定义', 'wf:processDefine:page', '0,2206080912582512640,2206080912695758848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.590', NULL, '2025-07-12 21:58:03.553', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912712536064, 'platform', 2206080912695758848, '查看流程定义详情', 'wf:processDefine:detail', '0,2206080912582512640,2206080912695758848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.593', NULL, '2025-07-12 21:58:03.558', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912720924672, 'platform', 2206080912695758848, '删除流程定义', 'wf:processDefine:remove', '0,2206080912582512640,2206080912695758848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.594', NULL, '2025-07-12 21:58:03.564', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912729313280, 'platform', 2206080912695758848, '启用/禁用流程定义', 'wf:processDefine:upAndDown', '0,2206080912582512640,2206080912695758848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.597', NULL, '2025-07-12 21:58:03.578', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912737701888, 'platform', 2206080912695758848, '发起流程', 'wf:processDefine:startAndExecute', '0,2206080912582512640,2206080912695758848', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.599', NULL, '2025-07-12 21:58:03.584', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912750284800, 'platform', 2206080912582512640, '我发起的', 'wf:processInstance', '0,2206080912582512640', 2, 230, '/wf/process-instance/index', '/wf/process-instance/index', 'ant-design:form-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"wf:processInstance:detail\":\"查看流程定义详情\",\"wf:processInstance:page\":\"分页查询流程定义\",\"wf:processInstance:startAndExecute\":\"发起流程\",\"wf:processInstance:withdraw\":\"撤回流程\"},\"component\":\"/wf/process-instance/index\",\"icon\":\"ant-design:form-outlined\",\"order\":230,\"perms\":[\"admin\",\"wf:processInstance\"]}', '2025-07-12 21:57:56.601', NULL, '2025-07-12 21:58:03.588', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912762867712, 'platform', 2206080912750284800, '分页查询流程定义', 'wf:processInstance:page', '0,2206080912582512640,2206080912750284800', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.604', NULL, '2025-07-12 21:58:03.595', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912771256320, 'platform', 2206080912750284800, '查看流程定义详情', 'wf:processInstance:detail', '0,2206080912582512640,2206080912750284800', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.606', NULL, '2025-07-12 21:58:03.597', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912779644928, 'platform', 2206080912750284800, '发起流程', 'wf:processInstance:startAndExecute', '0,2206080912582512640,2206080912750284800', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.608', NULL, '2025-07-12 21:58:03.602', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912788033536, 'platform', 2206080912750284800, '撤回流程', 'wf:processInstance:withdraw', '0,2206080912582512640,2206080912750284800', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.610', NULL, '2025-07-12 21:58:03.605', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912796422144, 'platform', 2206080912582512640, '我的待办', 'wf:processTask:todoList', '0,2206080912582512640', 2, 240, '/wf/process-task/todo', '/wf/process-task/todo', 'ant-design:mail-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"btns\":{\"wf:processTask:execute\":\"办理\",\"wf:processTask:surrogate\":\"委托\"},\"component\":\"/wf/process-task/todo\",\"icon\":\"ant-design:mail-outlined\",\"order\":240,\"perms\":[\"admin\",\"wf:processTask:todoList\"]}', '2025-07-12 21:57:56.612', NULL, '2025-07-12 21:58:03.608', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912804810752, 'platform', 2206080912796422144, '办理', 'wf:processTask:execute', '0,2206080912582512640,2206080912796422144', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.615', NULL, '2025-07-12 21:58:03.612', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912813199360, 'platform', 2206080912796422144, '委托', 'wf:processTask:surrogate', '0,2206080912582512640,2206080912796422144', 4, 999, NULL, NULL, NULL, 1, NULL, NULL, 1, NULL, NULL, 1, '{}', '2025-07-12 21:57:56.616', NULL, '2025-07-12 21:58:03.615', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912825782272, 'platform', 2206080912582512640, '我的已办', 'wf:processTask:doneList', '0,2206080912582512640', 2, 250, '/wf/process-task/done', '/wf/process-task/done', 'ant-design:read-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"/wf/process-task/done\",\"icon\":\"ant-design:read-outlined\",\"order\":250,\"perms\":[\"admin\",\"wf:processTask:doneList\"]}', '2025-07-12 21:57:56.619', NULL, '2025-07-12 21:58:03.618', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912838365184, 'platform', 2206080912582512640, '我的抄送', 'wf:processInstance:ccList', '0,2206080912582512640', 2, 260, '/wf/process-instance/cc-list', '/wf/process-instance/cc-list', 'ant-design:edit-outlined', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"/wf/process-instance/cc-list\",\"icon\":\"ant-design:edit-outlined\",\"order\":260,\"perms\":[\"admin\",\"wf:processInstance:ccList\"]}', '2025-07-12 21:57:56.622', NULL, '2025-07-12 21:58:03.621', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912842559488, 'platform', 0, 'demos.vben.title', 'VbenProject', '0', 1, 9998, '/vben-admin', 'BasicLayout', 'https://unpkg.com/@vbenjs/static-source@0.1.7/source/logo-v1.webp', 1, 0, NULL, 1, 1, 1, 1, '{\"badgeType\":\"dot\",\"component\":\"BasicLayout\",\"icon\":\"https://unpkg.com/@vbenjs/static-source@0.1.7/source/logo-v1.webp\",\"order\":9998,\"redirect\":\"/vben-admin/about\"}', '2025-07-12 21:57:56.624', NULL, '2025-07-12 21:58:03.624', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912855142400, 'platform', 2206080912842559488, 'demos.vben.about', 'VbenAbout', '0,2206080912842559488', 2, 999, '/vben-admin/about', '/_core/about/index', 'lucide:copyright', 1, 0, NULL, 1, 1, 1, 1, '{\"component\":\"/_core/about/index\",\"icon\":\"lucide:copyright\"}', '2025-07-12 21:57:56.627', NULL, '2025-07-12 21:58:03.627', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912863531008, 'platform', 2206080912842559488, 'demos.vben.document', 'VbenDocument', '0,2206080912842559488', 2, 999, '/vben-admin/document', NULL, 'lucide:book-open-text', 1, 1, NULL, 1, 1, 1, 1, '{\"icon\":\"lucide:book-open-text\",\"link\":\"https://doc.mldong.com/mldong/front-pro/pro-explain.html\"}', '2025-07-12 21:57:56.629', NULL, '2025-07-12 21:58:03.631', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912876113920, 'platform', 2206080912842559488, '源码', 'VbenGithub', '0,2206080912842559488', 2, 999, '/vben-admin/github', 'IFrameView', 'svg:gitee', 1, 1, NULL, 1, 1, 1, 1, '{\"component\":\"IFrameView\",\"icon\":\"svg:gitee\",\"link\":\"https://gitee.com/mldong/mldong-vben5\"}', '2025-07-12 21:57:56.631', NULL, '2025-07-12 21:58:03.633', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912880308224, 'platform', 2206080912842559488, 'demos.vben.naive-ui', 'VbenNaive', '0,2206080912842559488', 2, 999, '/vben-admin/naive', 'IFrameView', 'logos:naiveui', 1, 1, NULL, 1, 1, 1, 1, '{\"badgeType\":\"dot\",\"component\":\"IFrameView\",\"icon\":\"logos:naiveui\",\"link\":\"https://naive-vben5.mldong.com/\"}', '2025-07-12 21:57:56.633', NULL, '2025-07-12 21:58:03.636', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912897085440, 'platform', 2206080912842559488, 'demos.vben.element-plus', 'VbenElementPlus', '0,2206080912842559488', 2, 999, '/vben-admin/ele', 'IFrameView', 'logos:element', 1, 1, NULL, 1, 1, 1, 1, '{\"badgeType\":\"dot\",\"component\":\"IFrameView\",\"icon\":\"logos:element\",\"link\":\"https://ele-vben5.mldong.com/\"}', '2025-07-12 21:57:56.637', NULL, '2025-07-12 21:58:03.639', NULL, 0);
INSERT INTO `sys_menu` VALUES (2206080912905474048, 'platform', 0, 'demos.vben.about', 'VbenAbout2', '0', 2, 9999, '/vben-admin/about', NULL, 'lucide:copyright', 1, 0, NULL, 1, 1, 1, 1, '{\"icon\":\"lucide:copyright\",\"order\":9999}', '2025-07-12 21:57:56.639', NULL, '2025-07-12 21:58:03.642', NULL, 0);

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice`  (
  `id` bigint(0) NOT NULL COMMENT '通知公告ID',
  `title` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '内容',
  `type` int(0) NOT NULL COMMENT '类型<sys_notice_type>',
  `publish_time` datetime(3) NULL DEFAULT NULL COMMENT '发布时间',
  `state` int(0) NULL DEFAULT NULL COMMENT '发布状态<sys_notice_state>',
  `variable` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '扩展参数JSON',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '通知公告' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_notice
-- ----------------------------

-- ----------------------------
-- Table structure for sys_notice_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice_user`;
CREATE TABLE `sys_notice_user`  (
  `id` bigint(0) NOT NULL COMMENT '主键',
  `notice_id` bigint(0) NOT NULL COMMENT '通知公告ID',
  `user_id` bigint(0) NOT NULL COMMENT '用户ID',
  `is_read` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已读',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_notice_user_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'r_通知公告用户关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_notice_user
-- ----------------------------

-- ----------------------------
-- Table structure for sys_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_post`;
CREATE TABLE `sys_post`  (
  `id` bigint(0) NOT NULL COMMENT '岗位ID',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '岗位名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `sort` bigint(0) NULL DEFAULT 999 COMMENT '排序',
  `enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_sys_post_code`(`code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '岗位' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_post
-- ----------------------------
INSERT INTO `sys_post` VALUES (1, '岗位1', 'default1', 1, 0, NULL, '2025-07-04 23:20:07.000', 2, '2025-07-05 11:26:17.383', 2, 0);
INSERT INTO `sys_post` VALUES (2, '岗位2', 'default2', 999, 1, NULL, '2025-07-04 23:20:09.000', 2, '2025-07-04 23:20:14.000', 2, 0);

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `id` bigint(0) NOT NULL COMMENT '角色ID',
  `app_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '应用编码',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一编码',
  `sort` bigint(0) NULL DEFAULT 999 COMMENT '排序',
  `role_type` int(0) NOT NULL COMMENT '角色类型<sys_role_type>',
  `enabled` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `data_scope` int(0) NULL DEFAULT NULL COMMENT '数据范围(1: 全部数据权限; 2: 自定义数据权限; 3: 本部门数据权限; 4: 本部门及以下部门权限; 5: 仅本人数据权限)',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_sys_role_name`(`name`) USING BTREE,
  INDEX `idx_sys_role_code`(`code`) USING BTREE,
  INDEX `idx_sys_role_app_code`(`app_code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, 'platform', '默认角色', 'default', 999, 1, 1, NULL, NULL, NULL, NULL, '2025-07-15 22:31:39.581', NULL, 0);
INSERT INTO `sys_role` VALUES (2, 'platform', '角色1', 'code1', 999, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_role` VALUES (1550849411214725122, 'platform', '角色2', 'code2', 999, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_role` VALUES (1550849440218337282, 'platform', '角色3', 'code3', 999, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_role` VALUES (1550849464943759361, 'platform', '角色4', 'code4', 999, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_role` VALUES (1551054717827891201, 'platform', '角色5', 'code5', 999, 2, 1, NULL, NULL, NULL, NULL, '2022-10-22 22:32:32.466', 1, 1);
INSERT INTO `sys_role` VALUES (1583962216903647233, 'platform', '测试角色1', 'test11', 999, 2, 1, NULL, NULL, '2022-10-22 18:23:15.762', 1, '2022-10-22 18:23:15.762', 1, 0);
INSERT INTO `sys_role` VALUES (2207176622396674048, 'platform', '测试角色2', '2222', 22, 1, 1, NULL, NULL, '2025-07-15 22:31:54.139', NULL, '2025-07-15 22:31:54.139', NULL, 0);

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`  (
  `id` bigint(0) NOT NULL COMMENT '主键',
  `role_id` bigint(0) NOT NULL COMMENT '角色ID',
  `menu_id` bigint(0) NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_role_menu_rid`(`role_id`) USING BTREE,
  INDEX `idx_role_menu_mid`(`menu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'r_角色菜单关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES (1859228493727719440, 2, 1583066302173294594);
INSERT INTO `sys_role_menu` VALUES (2206823454919888896, 1, 2206080911387136000);
INSERT INTO `sys_role_menu` VALUES (2206823454928277504, 1, 2206080911395524608);
INSERT INTO `sys_role_menu` VALUES (2206823454932471808, 1, 2206080911403913216);
INSERT INTO `sys_role_menu` VALUES (2206823454936666112, 1, 2206080911416496128);
INSERT INTO `sys_role_menu` VALUES (2206823454945054720, 1, 2206080911429079040);
INSERT INTO `sys_role_menu` VALUES (2206823454949249024, 1, 2206080911441661952);
INSERT INTO `sys_role_menu` VALUES (2206823454953443328, 1, 2206080911450050560);
INSERT INTO `sys_role_menu` VALUES (2206823454953443329, 1, 2206080911462633472);
INSERT INTO `sys_role_menu` VALUES (2206823454957637632, 1, 2206080911471022080);
INSERT INTO `sys_role_menu` VALUES (2206823454961831936, 1, 2206080911479410688);
INSERT INTO `sys_role_menu` VALUES (2206823454966026240, 1, 2206080911378747392);
INSERT INTO `sys_role_menu` VALUES (2206823454974414848, 1, 2206080911370358784);
INSERT INTO `sys_role_menu` VALUES (2206823454974414849, 1, 2206080911487799296);
INSERT INTO `sys_role_menu` VALUES (2206823454978609152, 1, 2206080911546519552);
INSERT INTO `sys_role_menu` VALUES (2206823454982803456, 1, 2206080911676542976);
INSERT INTO `sys_role_menu` VALUES (2206823454986997760, 1, 2206080911743651840);
INSERT INTO `sys_role_menu` VALUES (2206823454991192064, 1, 2206080911798177792);
INSERT INTO `sys_role_menu` VALUES (2206823454991192065, 1, 2206080911882063872);
INSERT INTO `sys_role_menu` VALUES (2206823454999580672, 1, 2206080911949172736);
INSERT INTO `sys_role_menu` VALUES (2206823455003774976, 1, 2206080912095973376);
INSERT INTO `sys_role_menu` VALUES (2206823455007969280, 1, 2206080912171470848);
INSERT INTO `sys_role_menu` VALUES (2206823455012163584, 1, 2206080911504576512);
INSERT INTO `sys_role_menu` VALUES (2206823455016357888, 1, 2206080911512965120);
INSERT INTO `sys_role_menu` VALUES (2206823455020552192, 1, 2206080911521353728);
INSERT INTO `sys_role_menu` VALUES (2206823455020552193, 1, 2206080911529742336);
INSERT INTO `sys_role_menu` VALUES (2206823455028940800, 1, 2206080911538130944);
INSERT INTO `sys_role_menu` VALUES (2206823455028940801, 1, 2206080911563296768);
INSERT INTO `sys_role_menu` VALUES (2206823455033135104, 1, 2206080911575879680);
INSERT INTO `sys_role_menu` VALUES (2206823455037329408, 1, 2206080911588462592);
INSERT INTO `sys_role_menu` VALUES (2206823455041523712, 1, 2206080911592656896);
INSERT INTO `sys_role_menu` VALUES (2206823455045718016, 1, 2206080911601045504);
INSERT INTO `sys_role_menu` VALUES (2206823455045718017, 1, 2206080911609434112);
INSERT INTO `sys_role_menu` VALUES (2206823455049912320, 1, 2206080911617822720);
INSERT INTO `sys_role_menu` VALUES (2206823455054106624, 1, 2206080911626211328);
INSERT INTO `sys_role_menu` VALUES (2206823455054106625, 1, 2206080911642988544);
INSERT INTO `sys_role_menu` VALUES (2206823455058300928, 1, 2206080911655571456);
INSERT INTO `sys_role_menu` VALUES (2206823455062495232, 1, 2206080911668154368);
INSERT INTO `sys_role_menu` VALUES (2206823455066689536, 1, 2206080911684931584);
INSERT INTO `sys_role_menu` VALUES (2206823455070883840, 1, 2206080911693320192);
INSERT INTO `sys_role_menu` VALUES (2206823455075078144, 1, 2206080911701708800);
INSERT INTO `sys_role_menu` VALUES (2206823455079272448, 1, 2206080911714291712);
INSERT INTO `sys_role_menu` VALUES (2206823455087661056, 1, 2206080911726874624);
INSERT INTO `sys_role_menu` VALUES (2206823455091855360, 1, 2206080911739457536);
INSERT INTO `sys_role_menu` VALUES (2206823455096049664, 1, 2206080911756234752);
INSERT INTO `sys_role_menu` VALUES (2206823455100243968, 1, 2206080911764623360);
INSERT INTO `sys_role_menu` VALUES (2206823455100243969, 1, 2206080911777206272);
INSERT INTO `sys_role_menu` VALUES (2206823455104438272, 1, 2206080911789789184);
INSERT INTO `sys_role_menu` VALUES (2206823455112826880, 1, 2206080911806566400);
INSERT INTO `sys_role_menu` VALUES (2206823455117021184, 1, 2206080911814955008);
INSERT INTO `sys_role_menu` VALUES (2206823455121215488, 1, 2206080911823343616);
INSERT INTO `sys_role_menu` VALUES (2206823455121215489, 1, 2206080911831732224);
INSERT INTO `sys_role_menu` VALUES (2206823455125409792, 1, 2206080911844315136);
INSERT INTO `sys_role_menu` VALUES (2206823455129604096, 1, 2206080911856898048);
INSERT INTO `sys_role_menu` VALUES (2206823455133798400, 1, 2206080911865286656);
INSERT INTO `sys_role_menu` VALUES (2206823455137992704, 1, 2206080911873675264);
INSERT INTO `sys_role_menu` VALUES (2206823455142187008, 1, 2206080911894646784);
INSERT INTO `sys_role_menu` VALUES (2206823455150575616, 1, 2206080911903035392);
INSERT INTO `sys_role_menu` VALUES (2206823455154769920, 1, 2206080911919812608);
INSERT INTO `sys_role_menu` VALUES (2206823455163158528, 1, 2206080911928201216);
INSERT INTO `sys_role_menu` VALUES (2206823455167352832, 1, 2206080911936589824);
INSERT INTO `sys_role_menu` VALUES (2206823455171547136, 1, 2206080911957561344);
INSERT INTO `sys_role_menu` VALUES (2206823455171547137, 1, 2206080911965949952);
INSERT INTO `sys_role_menu` VALUES (2206823455179935744, 1, 2206080911974338560);
INSERT INTO `sys_role_menu` VALUES (2206823455184130048, 1, 2206080911991115776);
INSERT INTO `sys_role_menu` VALUES (2206823455184130049, 1, 2206080912003698688);
INSERT INTO `sys_role_menu` VALUES (2206823455188324352, 1, 2206080912012087296);
INSERT INTO `sys_role_menu` VALUES (2206823455192518656, 1, 2206080912020475904);
INSERT INTO `sys_role_menu` VALUES (2206823455196712960, 1, 2206080912028864512);
INSERT INTO `sys_role_menu` VALUES (2206823455200907264, 1, 2206080912037253120);
INSERT INTO `sys_role_menu` VALUES (2206823455205101568, 1, 2206080912045641728);
INSERT INTO `sys_role_menu` VALUES (2206823455209295872, 1, 2206080912062418944);
INSERT INTO `sys_role_menu` VALUES (2206823455213490176, 1, 2206080912070807552);
INSERT INTO `sys_role_menu` VALUES (2206823455217684480, 1, 2206080912083390464);
INSERT INTO `sys_role_menu` VALUES (2206823455226073088, 1, 2206080912108556288);
INSERT INTO `sys_role_menu` VALUES (2206823455234461696, 1, 2206080912116944896);
INSERT INTO `sys_role_menu` VALUES (2206823455238656000, 1, 2206080912129527808);
INSERT INTO `sys_role_menu` VALUES (2206823455247044608, 1, 2206080912146305024);
INSERT INTO `sys_role_menu` VALUES (2206823455251238912, 1, 2206080912163082240);
INSERT INTO `sys_role_menu` VALUES (2206823455255433216, 1, 2206080912179859456);
INSERT INTO `sys_role_menu` VALUES (2206823455259627520, 1, 2206080912196636672);
INSERT INTO `sys_role_menu` VALUES (2206823455263821824, 1, 2206080912209219584);
INSERT INTO `sys_role_menu` VALUES (2206823455268016128, 1, 2206080912221802496);
INSERT INTO `sys_role_menu` VALUES (2206823455268016129, 1, 2206080912230191104);
INSERT INTO `sys_role_menu` VALUES (2206823455272210432, 1, 2206080912238579712);
INSERT INTO `sys_role_menu` VALUES (2206823455276404736, 1, 2206080912246968320);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` bigint(0) NOT NULL COMMENT '用户ID',
  `user_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `real_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `nick_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户头像',
  `password` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户密码',
  `salt` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码加盐',
  `mobile_phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '手机号',
  `tel` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系电话',
  `email` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `admin_type` int(0) NULL DEFAULT NULL COMMENT '管理员类型<sys_admin_type>',
  `sex` int(0) NOT NULL DEFAULT 3 COMMENT '性别<sys_sex>',
  `is_locked` tinyint(0) NOT NULL DEFAULT 0 COMMENT '是否锁定',
  `dept_id` bigint(0) NULL DEFAULT NULL COMMENT '所属部门',
  `post_id` bigint(0) NULL DEFAULT NULL COMMENT '所属岗位',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(3) NULL DEFAULT NULL COMMENT '创建时间',
  `create_user` bigint(0) NULL DEFAULT NULL COMMENT '创建用户',
  `update_time` datetime(3) NULL DEFAULT NULL COMMENT '更新时间',
  `update_user` bigint(0) NULL DEFAULT NULL COMMENT '更新用户',
  `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (2, 'admin', '乔丽', '实', 'http://dummyimage.com/200x100', '30d481747cd1b7ed948021f272d2504a', 'bvq00p03', '18123144942', '18613653778', 'l.jpryby@trxm.ye', 2, 1, 0, 1, 2, '关温识才目同重天计声响与。', NULL, NULL, '2025-03-09 08:55:13.615', 1, 0);
INSERT INTO `sys_user` VALUES (1583686921567027202, 'superAdmin', '超级管理员', '实', 'http://dummyimage.com/120x60', '30d481747cd1b7ed948021f272d2504a', 'bvq00p03', '18123144943', '18613653778', 'l.jpryby@trxm.ye', 1, 3, 0, NULL, NULL, '关温识才目同重天计声响与。', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_user` VALUES (1583687667914043393, 'admin4', '任娟', '实', 'http://dummyimage.com/200x100', '5f0a17dbc0cbe6c7f5bdbf4245a81d68', 'a9hezpa7', '18123144945', '18125160137', 'l.jpryby@trxm.ye', 2, 2, 0, 1, 2, '关温识才目同重天计声响与。', NULL, NULL, '2025-07-12 11:40:32.947', 1, 0);
INSERT INTO `sys_user` VALUES (1987890266278858752, 'test2222', '沈秀英', '沈秀英', 'http://dummyimage.com/250x250', '576b80728b67d7b6188bde5d392efb94', 'fkvn51Dl', '18123104776', '18695269767', 'g.gkfy@tfjti.sm', 2, 1, 0, NULL, NULL, '此清外清月段构太点一之他识要产。适队比技京飞动类五便八处连。即级为成证几二转实号便才这业。者设商行想义律前支称型可公各能铁值。度东飞通重收结得理因她每型并。率她类做约山则局者林照此放任断布经。', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_user` VALUES (1987890712238231552, 'test2222', '沈秀英22', '沈秀英', 'http://dummyimage.com/250x250', 'c6dfc6ca0627774b1a018df3d88d440e', 'jyhztxnQ', '18123104776', '18695269767', 'g.gkfy@tfjti.sm', 2, 1, 0, NULL, NULL, '此清外清月段构太点一之他识要产。适队比技京飞动类五便八处连。即级为成证几二转实号便才这业。者设商行想义律前支称型可公各能铁值。度东飞通重收结得理因她每型并。率她类做约山则局者林照此放任断布经。', '2025-11-10 22:30:53.678', 2, '2025-11-10 22:31:12.021', 2, 0);

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `id` bigint(0) NOT NULL COMMENT '主键',
  `user_id` bigint(0) NOT NULL COMMENT '用户ID',
  `role_id` bigint(0) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_sys_user_role_uid`(`user_id`) USING BTREE,
  INDEX `idx_sys_user_role_rid`(`role_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'r_用户角色关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1869034738580008962, 1583687667914043393, 2);
INSERT INTO `sys_user_role` VALUES (1869034778513977348, 1583687667914043393, 1550849464943759361);
INSERT INTO `sys_user_role` VALUES (1894047910776868866, 2, 1);
INSERT INTO `sys_user_role` VALUES (1894047910776868867, 2, 2);
INSERT INTO `sys_user_role` VALUES (1894047978904948737, 3, 2);
INSERT INTO `sys_user_role` VALUES (1894047978904948738, 3, 1550849464943759361);
INSERT INTO `sys_user_role` VALUES (1894047978904948739, 3, 1550849411214725122);
INSERT INTO `sys_user_role` VALUES (1894047978904948740, 3, 1550849440218337282);
INSERT INTO `sys_user_role` VALUES (2173481668302606336, 2173481668281634816, 1);
INSERT INTO `sys_user_role` VALUES (2173481668315189248, 2173481668281634816, 2);
INSERT INTO `sys_user_role` VALUES (2173484298580004864, 2173484298563227648, 1);
INSERT INTO `sys_user_role` VALUES (2173484298600976384, 2173484298563227648, 2);
INSERT INTO `sys_user_role` VALUES (2206823483298549760, 3, 1);

SET FOREIGN_KEY_CHECKS = 1;
