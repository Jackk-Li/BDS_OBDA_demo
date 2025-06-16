#!/usr/bin/env python3
"""
OBDA推理效果可视化演示
通过图形化方式展示本体推理如何扩展查询结果
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import networkx as nx
import pandas as pd
import mysql.connector
from typing import Dict, List, Tuple
import json

class OBDAReasoningVisualizer:
    """OBDA推理效果可视化工具"""
    
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.fig_counter = 0
        
    def connect_db(self):
        """连接数据库"""
        return mysql.connector.connect(
            host=self.db_config['host'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
    
    def visualize_class_hierarchy(self):
        """可视化类层次结构"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # 创建有向图
        G = nx.DiGraph()
        
        # 添加节点和边
        hierarchy = {
            'Person': ['Employee', 'Student'],
            'Employee': ['AcademicStaff', 'AdministrativeStaff'],
            'AcademicStaff': ['Professor', 'AssociateProfessor', 'Lecturer'],
            'Student': ['UndergraduateStudent', 'GraduateStudent']
        }
        
        for parent, children in hierarchy.items():
            for child in children:
                G.add_edge(parent, child)
        
        # 使用层次布局
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        
        # 绘制节点
        node_colors = {
            'Person': '#ff9999',
            'Employee': '#66b3ff',
            'Student': '#99ff99',
            'AcademicStaff': '#ffcc99',
            'AdministrativeStaff': '#ff99cc',
            'Professor': '#c2c2f0',
            'AssociateProfessor': '#c2c2f0',
            'Lecturer': '#c2c2f0',
            'UndergraduateStudent': '#90ee90',
            'GraduateStudent': '#90ee90'
        }
        
        for node in G.nodes():
            nx.draw_networkx_nodes(G, pos, [node], 
                                 node_color=node_colors.get(node, '#cccccc'),
                                 node_size=3000,
                                 node_shape='o')
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                             arrows=True, arrowsize=20, 
                             arrowstyle='->', width=2)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # 添加说明
        ax.text(0.02, 0.98, '类层次结构', transform=ax.transAxes,
                fontsize=16, fontweight='bold', va='top')
        ax.text(0.02, 0.93, '箭头表示子类关系 (A → B 表示 B 是 A 的子类)',
                transform=ax.transAxes, fontsize=10, va='top')
        
        ax.axis('off')
        plt.title('OBDA本体类层次结构', fontsize=18, pad=20)
        plt.tight_layout()
        plt.savefig(f'reasoning_vis_{self.fig_counter}_hierarchy.png', dpi=150, bbox_inches='tight')
        self.fig_counter += 1
        plt.show()
    
    def visualize_reasoning_effect(self):
        """可视化推理效果对比"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 左侧：无推理查询
        ax1.set_title('无推理：查询Person类', fontsize=14, fontweight='bold')
        ax1.text(0.5, 0.7, 'SELECT * WHERE { ?x a :Person }', 
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax1.text(0.5, 0.5, '↓', ha='center', va='center', fontsize=20)
        ax1.text(0.5, 0.3, '结果：0条', ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        ax1.text(0.5, 0.1, '(数据库中没有直接标记为Person的记录)', 
                ha='center', va='center', fontsize=10, style='italic')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        
        # 右侧：有推理查询
        ax2.set_title('有推理：查询Person类', fontsize=14, fontweight='bold')
        ax2.text(0.5, 0.85, 'SELECT * WHERE { ?x a :Person }', 
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax2.text(0.5, 0.75, '↓', ha='center', va='center', fontsize=20)
        ax2.text(0.5, 0.65, '推理引擎扩展查询', ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        ax2.text(0.5, 0.55, '↓', ha='center', va='center', fontsize=20)
        
        # 显示推理过程
        reasoning_steps = [
            "Person ⊇ Employee",
            "Person ⊇ Student",
            "Employee ⊇ AcademicStaff",
            "Employee ⊇ AdministrativeStaff",
            "..."
        ]
        
        y_pos = 0.45
        for step in reasoning_steps:
            ax2.text(0.5, y_pos, step, ha='center', va='center', fontsize=9)
            y_pos -= 0.05
        
        ax2.text(0.5, 0.15, '结果：9条', ha='center', va='center', fontsize=14,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
        ax2.text(0.5, 0.05, '(包含所有Employee和Student)', 
                ha='center', va='center', fontsize=10, style='italic')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        plt.suptitle('OBDA推理效果对比', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'reasoning_vis_{self.fig_counter}_comparison.png', dpi=150, bbox_inches='tight')
        self.fig_counter += 1
        plt.show()
    
    def visualize_query_rewriting(self):
        """可视化查询重写过程"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        
        # SPARQL查询
        sparql_box = FancyBboxPatch((0.1, 0.8), 0.8, 0.15,
                                   boxstyle="round,pad=0.02",
                                   facecolor='lightblue',
                                   edgecolor='black')
        ax.add_patch(sparql_box)
        ax.text(0.5, 0.875, 'SPARQL查询', ha='center', va='center', 
               fontsize=12, fontweight='bold')
        ax.text(0.5, 0.825, 'SELECT ?teacher ?name WHERE {\n  ?teacher a :Teacher ;\n           :hasName ?name }',
               ha='center', va='center', fontsize=10, family='monospace')
        
        # 推理步骤
        reasoning_box = FancyBboxPatch((0.1, 0.5), 0.8, 0.25,
                                     boxstyle="round,pad=0.02",
                                     facecolor='lightyellow',
                                     edgecolor='black')
        ax.add_patch(reasoning_box)
        ax.text(0.5, 0.72, '查询重写（使用本体定义）', ha='center', va='center',
               fontsize=12, fontweight='bold')
        ax.text(0.5, 0.65, 'Teacher ≡ Employee ⊓ ∃teaches.Course', 
               ha='center', va='center', fontsize=10)
        ax.text(0.5, 0.60, '↓', ha='center', va='center', fontsize=16)
        ax.text(0.5, 0.55, '展开为：查找所有有教学记录的员工', 
               ha='center', va='center', fontsize=10)
        
        # SQL查询
        sql_box = FancyBboxPatch((0.1, 0.15), 0.8, 0.3,
                               boxstyle="round,pad=0.02",
                               facecolor='lightgreen',
                               edgecolor='black')
        ax.add_patch(sql_box)
        ax.text(0.5, 0.42, '生成的SQL查询', ha='center', va='center',
               fontsize=12, fontweight='bold')
        sql_query = """SELECT DISTINCT 
  CONCAT('employee/', e.emp_id) AS teacher,
  e.name
FROM employees e
WHERE EXISTS (
  SELECT 1 
  FROM teaching_records t 
  WHERE t.emp_id = e.emp_id
)
ORDER BY e.name"""
        ax.text(0.5, 0.28, sql_query, ha='center', va='center', 
               fontsize=9, family='monospace')
        
        # 添加箭头
        arrow1 = ConnectionPatch((0.5, 0.8), (0.5, 0.75), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc="black", lw=2)
        ax.add_artist(arrow1)
        
        arrow2 = ConnectionPatch((0.5, 0.5), (0.5, 0.45), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc="black", lw=2)
        ax.add_artist(arrow2)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        plt.title('OBDA查询重写过程', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f'reasoning_vis_{self.fig_counter}_rewriting.png', dpi=150, bbox_inches='tight')
        self.fig_counter += 1
        plt.show()
    
    def compare_query_results(self):
        """比较SQL和SPARQL查询结果"""
        # 连接数据库获取真实数据
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # SQL查询（无推理）
        sql_queries = {
            "直接查询Professor": 
                "SELECT name FROM employees WHERE position = 'Professor'",
            "查询有教学任务的员工":
                """SELECT DISTINCT e.name 
                   FROM employees e 
                   JOIN teaching_records t ON e.emp_id = t.emp_id""",
            "查询所有员工":
                "SELECT name FROM employees"
        }
        
        # SPARQL查询结果（模拟）
        sparql_results = {
            "查询Person类": ["Alice Wang", "Bob Chen", "Carol Liu", "David Zhang", 
                           "Emma Li", "Frank Zhou", "Grace Ma", "Henry Wu", "Ivy Chen"],
            "查询Teacher类": ["Alice Wang", "Bob Chen", "Carol Liu", "David Zhang"],
            "查询AcademicStaff类": ["Alice Wang", "Bob Chen", "Carol Liu", "David Zhang"]
        }
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        # 执行SQL查询并可视化
        for i, (query_name, query) in enumerate(sql_queries.items()):
            if i >= len(axes) - 1:
                break
                
            cursor.execute(query)
            results = [row[0] for row in cursor.fetchall()]
            
            ax = axes[i]
            ax.set_title(f'SQL: {query_name}', fontsize=12, fontweight='bold')
            
            y_pos = 0.9
            ax.text(0.5, y_pos, f'结果数量: {len(results)}', 
                   ha='center', fontsize=11, fontweight='bold')
            y_pos -= 0.1
            
            for result in results[:5]:  # 只显示前5个
                ax.text(0.5, y_pos, f'• {result}', ha='center', fontsize=10)
                y_pos -= 0.08
            
            if len(results) > 5:
                ax.text(0.5, y_pos, f'... 还有 {len(results)-5} 条', 
                       ha='center', fontsize=10, style='italic')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # SPARQL结果对比
        ax = axes[3]
        ax.set_title('SPARQL+推理: 查询Person类', fontsize=12, fontweight='bold')
        
        results = sparql_results["查询Person类"]
        y_pos = 0.9
        ax.text(0.5, y_pos, f'结果数量: {len(results)}', 
               ha='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
        y_pos -= 0.1
        
        # 按类型分组显示
        ax.text(0.3, y_pos, '员工:', ha='center', fontsize=10, fontweight='bold')
        ax.text(0.7, y_pos, '学生:', ha='center', fontsize=10, fontweight='bold')
        y_pos -= 0.08
        
        employees = results[:5]
        students = results[5:]
        
        for emp in employees:
            ax.text(0.3, y_pos, f'• {emp}', ha='center', fontsize=9)
            y_pos -= 0.06
            
        y_pos = 0.72  # 重置位置
        for stu in students:
            ax.text(0.7, y_pos, f'• {stu}', ha='center', fontsize=9)
            y_pos -= 0.06
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        plt.suptitle('SQL vs SPARQL查询结果对比', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'reasoning_vis_{self.fig_counter}_results.png', dpi=150, bbox_inches='tight')
        self.fig_counter += 1
        plt.show()
        
        conn.close()
    
    def create_summary_diagram(self):
        """创建OBDA工作流程总结图"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        
        # 定义组件位置
        components = {
            'user': (0.5, 0.9, 'lightblue', '用户'),
            'sparql': (0.5, 0.75, 'lightgreen', 'SPARQL查询'),
            'ontology': (0.2, 0.55, 'lightyellow', '本体\n(概念模型)'),
            'mappings': (0.5, 0.55, 'lightcoral', '映射规则\n(R2RML)'),
            'reasoner': (0.8, 0.55, 'lightgray', '推理引擎'),
            'sql': (0.5, 0.35, 'lightcyan', 'SQL查询'),
            'database': (0.5, 0.15, 'wheat', '关系数据库')
        }
        
        # 绘制组件
        for comp, (x, y, color, label) in components.items():
            if comp == 'database':
                # 数据库用矩形
                rect = FancyBboxPatch((x-0.12, y-0.05), 0.24, 0.1,
                                    boxstyle="round,pad=0.02",
                                    facecolor=color,
                                    edgecolor='black',
                                    linewidth=2)
            else:
                # 其他用圆形
                rect = plt.Circle((x, y), 0.08, facecolor=color, 
                                edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center', 
                   fontsize=10, fontweight='bold')
        
        # 添加连接箭头和说明
        arrows = [
            ((0.5, 0.82), (0.5, 0.83), '发起查询'),
            ((0.5, 0.67), (0.5, 0.63), ''),
            ((0.42, 0.55), (0.28, 0.55), '使用'),
            ((0.58, 0.55), (0.72, 0.55), '推理'),
            ((0.5, 0.47), (0.5, 0.43), '生成'),
            ((0.5, 0.27), (0.5, 0.20), '执行')
        ]
        
        for (x1, y1), (x2, y2), label in arrows:
            arrow = ConnectionPatch((x1, y1), (x2, y2), "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="black", lw=2)
            ax.add_artist(arrow)
            if label:
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax.text(mid_x + 0.05, mid_y, label, fontsize=9)
        
        # 添加工作流程说明
        workflow_text = """工作流程：
1. 用户使用领域概念发起SPARQL查询
2. Ontop使用本体和映射规则理解查询
3. 推理引擎扩展查询包含所有相关概念
4. 生成优化的SQL查询
5. 在数据库上执行并返回结果"""
        
        ax.text(0.02, 0.3, workflow_text, transform=ax.transAxes,
               fontsize=10, va='top',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
        
        # 添加优势说明
        benefits_text = """OBDA优势：
• 概念查询：使用业务概念而非表结构
• 智能推理：自动包含相关子类和等价类
• 数据整合：统一访问分散的数据
• 易于扩展：添加新概念无需改数据库"""
        
        ax.text(0.98, 0.3, benefits_text, transform=ax.transAxes,
               fontsize=10, va='top', ha='right',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        plt.title('OBDA系统工作流程', fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f'reasoning_vis_{self.fig_counter}_workflow.png', dpi=150, bbox_inches='tight')
        self.fig_counter += 1
        plt.show()

def main():
    """主函数"""
    # 数据库配置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': input("请输入MySQL密码: "),
        'database': 'university_demo'
    }
    
    # 创建可视化器
    visualizer = OBDAReasoningVisualizer(db_config)
    
    print("OBDA推理效果可视化演示")
    print("=" * 50)
    
    # 生成所有可视化
    print("\n1. 生成类层次结构图...")
    visualizer.visualize_class_hierarchy()
    
    print("\n2. 生成推理效果对比图...")
    visualizer.visualize_reasoning_effect()
    
    print("\n3. 生成查询重写过程图...")
    visualizer.visualize_query_rewriting()
    
    print("\n4. 生成查询结果对比图...")
    visualizer.compare_query_results()
    
    print("\n5. 生成OBDA工作流程总结图...")
    visualizer.create_summary_diagram()
    
    print("\n所有可视化图表已生成！")
    print("图片保存在当前目录：reasoning_vis_*.png")

if __name__ == "__main__":
    main()